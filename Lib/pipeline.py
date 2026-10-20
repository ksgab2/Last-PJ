"""
LIAOLLET — 취향 아카이브 파이프라인 (lib/pipeline.py)

Entry 페이지에서 받은 입력(사진, 문장, 태그, aspect)을
하나의 '도록 해설' 로 묶어 entry_result dict를 반환한다.

반환 dict 구조 (page4_result.html / page5_shelves.html이 소비):
{
    "persona": "lia" | "ol" | "let",
    "date": "YYYY.MM.DD",
    "quote": str,                  # 사용자 문장 또는 폴백
    "poetic_story": str,           # Gemini가 생성한 큐레토리얼 코멘트
    "tags": [str, ...],            # 사용자 선택 또는 폴백
    "photos": ["data:image/jpeg;base64,...", ...],   # EXIF 제거·리사이즈됨
    "image_summaries": [str, ...], # (디버그용) 이미지별 한 줄 요약
    "likes": int,
}

설계 원칙:
- YOLO/색추출은 포함하지 않는다 (Streamlit Cloud RAM 1GB 절약).
  전처리는 scripts/preprocess.py가 로컬 배치로 처리하고 결과만 커밋.
- Gemini Vision + Gemini Text 두 가지만 사용.
- EXIF(GPS) 제거, 리사이즈, 캐시, 재시도, 폴백 포함.
"""
from __future__ import annotations

import base64
import datetime
from io import BytesIO
from typing import Iterable

import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)


# ------------------------------------------------------------------
# 0. 상수
# ------------------------------------------------------------------
PERSONA_INFO = {
    "lia": {
        "name": "Lia",
        "role": "Text & Silhouette",
        "voice": "짧고 조용한 문장. 여백을 남긴다. 감정을 직접 말하지 않고 장면으로 옮긴다.",
        "keywords": ["여백", "실루엣", "문장", "새벽", "느린 풍경"],
    },
    "ol": {
        "name": "Ol",
        "role": "Visual & Texture",
        "voice": "단어만 툭. 질감과 색을 먼저 본다. 손으로 붙이는 사람.",
        "keywords": ["종이질감", "오린 단면", "테이프", "콜라주", "따뜻한 검정"],
    },
    "let": {
        "name": "Let",
        "role": "Synthesis & Layer",
        "voice": "질문과 느낌표. 공간과 사람을 잇는다. 다층 레이어.",
        "keywords": ["오버레이", "공간", "큐레이션", "조명", "버건디"],
    },
}

FALLBACK_STORY = {
    "lia": "입력된 문장의 잔상이 여백으로 정돈됩니다. 지나온 순간들은 실루엣으로 남아 기록의 한 면을 이룹니다.",
    "ol": "수집된 조각들의 질감과 색면이 하나의 도록으로 재구성되었습니다. 손끝의 온도가 시각적 층위로 남습니다.",
    "let": "서로 다른 층위의 조각들이 겹쳐지며 하나의 장면으로 정리됩니다. 다층의 언어가 은은하게 공명합니다.",
}

MAX_IMAGE_SIDE = 1024
MAX_IMAGES = 5


# ------------------------------------------------------------------
# 1. 클라이언트 / 설정
# ------------------------------------------------------------------
@st.cache_resource
def _get_client() -> genai.Client:
    api_key = st.secrets.get("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GOOGLE_API_KEY가 secrets에 없습니다. "
            ".streamlit/secrets.toml(로컬) 또는 Streamlit Cloud Secrets에 추가하세요."
        )
    return genai.Client(api_key=api_key)


def _get_model_name() -> str:
    return st.secrets.get("GEMINI_MODEL", "gemini-3.8-flash")


def _get_api_key() -> str:
    key = st.secrets.get("GOOGLE_API_KEY")
    if not key:
        raise RuntimeError("GOOGLE_API_KEY 없음")
    return key


# ------------------------------------------------------------------
# 2. 이미지 유틸
# ------------------------------------------------------------------
def _strip_exif_and_resize(raw: bytes) -> bytes:
    """EXIF(GPS 포함) 제거 + 최대 변 1024px 리사이즈 + JPEG 재저장."""
    img = Image.open(BytesIO(raw))
    if img.mode != "RGB":
        img = img.convert("RGB")

    w, h = img.size
    if max(w, h) > MAX_IMAGE_SIDE:
        scale = MAX_IMAGE_SIDE / max(w, h)
        img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)

    buf = BytesIO()
    img.save(buf, format="JPEG", quality=85, optimize=True)
    return buf.getvalue()


def _file_to_bytes(file_like) -> bytes:
    if hasattr(file_like, "getvalue"):
        return file_like.getvalue()
    return file_like.read()


def _bytes_to_data_url(jpeg_bytes: bytes) -> str:
    b64 = base64.b64encode(jpeg_bytes).decode("ascii")
    return f"data:image/jpeg;base64,{b64}"


def _prepare_photos(files: Iterable) -> tuple[list[str], list[bytes]]:
    """업로드 파일 → (data_urls, cleaned_bytes). 실패한 파일은 건너뜀."""
    data_urls: list[str] = []
    cleaned: list[bytes] = []
    for i, f in enumerate(files):
        if len(data_urls) >= MAX_IMAGES:
            break
        try:
            raw = _file_to_bytes(f)
            jpeg = _strip_exif_and_resize(raw)
            data_urls.append(_bytes_to_data_url(jpeg))
            cleaned.append(jpeg)
        except Exception as e:
            st.warning(f"이미지 {i+1} 처리 실패 (건너뜀): {e}")
    return data_urls, cleaned


# ------------------------------------------------------------------
# 3. Gemini 호출 (캐시 + 재시도)
# ------------------------------------------------------------------
@st.cache_data(ttl=86400, show_spinner=False)
def _cached_generate_text(prompt: str, model: str, api_key: str) -> str:
    client = genai.Client(api_key=api_key)
    resp = client.models.generate_content(model=model, contents=prompt)
    return (resp.text or "").strip()


@st.cache_data(ttl=86400, show_spinner=False)
def _cached_generate_with_image(
    prompt: str, image_b64: str, model: str, api_key: str
) -> str:
    client = genai.Client(api_key=api_key)
    image_bytes = base64.b64decode(image_b64)
    resp = client.models.generate_content(
        model=model,
        contents=[
            types.Part.from_text(text=prompt),
            types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
        ],
    )
    return (resp.text or "").strip()


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(min=1, max=8),
    retry=retry_if_exception_type(Exception),
    reraise=True,
)
def _generate_text_with_retry(prompt: str) -> str:
    return _cached_generate_text(prompt, _get_model_name(), _get_api_key())


@retry(
    stop=stop_after_attempt(2),
    wait=wait_exponential(min=1, max=5),
    reraise=True,
)
def _generate_image_summary_with_retry(prompt: str, image_bytes: bytes) -> str:
    image_b64 = base64.b64encode(image_bytes).decode("ascii")
    return _cached_generate_with_image(
        prompt, image_b64, _get_model_name(), _get_api_key()
    )


# ------------------------------------------------------------------
# 4. 프롬프트 빌더
# ------------------------------------------------------------------
def _build_curatorial_prompt(
    persona: str,
    text: str,
    tags: list[str],
    image_summaries: list[str],
) -> str:
    info = PERSONA_INFO[persona]
    tag_line = ", ".join(tags) if tags else "(선택 없음)"
    summaries = " / ".join(image_summaries) if image_summaries else "(이미지 요약 없음)"
    return f"""당신은 사적인 취향 아카이브의 큐레이터입니다.
아래 입력을 바탕으로 전시 도록에 실릴 **큐레토리얼 코멘트 한 단락**을 써 주세요.

[페르소나]
- 이름: {info['name']}
- 역할: {info['role']}
- 문체 지침: {info['voice']}
- 참조 키워드: {', '.join(info['keywords'])}

[사용자 입력]
- 사용자가 쓴 문장: {text or '(없음)'}
- 사용자가 고른 태그: {tag_line}
- 업로드 이미지 요약: {summaries}

[규칙 — 반드시 지킬 것]
1. 입력에 없는 사실을 지어내지 마세요.
2. 사용자의 문장을 그대로 반복하지 말고, 그 정서를 다른 언어로 옮기세요.
3. 퍼센트, 점수, 진단, "당신은 ~입니다" 같은 단정 표현 금지.
4. 과장된 형용사(눈부신, 압도적인, 완벽한 등)는 쓰지 마세요.
5. 2~3문장, 150~220자.
6. 마지막 문장은 짧은 명사구로 여운을 남기세요.
7. 출력은 해설 문단만. 머리말, 라벨, 따옴표, JSON, 마크다운 없이."""


def _build_image_summary_prompt(persona: str) -> str:
    info = PERSONA_INFO[persona]
    return f"""아래 이미지의 시각적 분위기를 한 문장(40자 이내)으로 요약하세요.
페르소나 관점: {info['role']} ({info['name']})

규칙:
- 색, 질감, 빛, 구도 위주로.
- 사람의 얼굴, 신원, 개인정보는 묘사하지 마세요.
- 추측·과장 금지.
- 출력은 요약 한 문장만."""


# ------------------------------------------------------------------
# 5. 메인 엔트리
# ------------------------------------------------------------------
def analyze_entry(
    files=None,
    text: str = "",
    tags: list[str] | None = None,
    aspect: str = "lia",
    use_vision: bool = True,
) -> dict:
    """Entry 페이지에서 호출. 반환 dict는 page4/page5가 그대로 소비."""
    files = list(files or [])
    tags = list(tags or [])
    aspect = aspect if aspect in PERSONA_INFO else "lia"
    text = (text or "").strip()

    # 1) 이미지 준비 (EXIF 제거 + 리사이즈 + base64)
    photo_data_urls, cleaned_bytes = _prepare_photos(files)

    # 2) 이미지 요약 (최대 2장, 선택)
    image_summaries: list[str] = []
    if use_vision and cleaned_bytes:
        prompt = _build_image_summary_prompt(aspect)
        for img_bytes in cleaned_bytes[:2]:
            try:
                summary = _generate_image_summary_with_retry(prompt, img_bytes)
                if summary:
                    image_summaries.append(summary)
            except Exception:
                pass  # 요약 실패는 치명적이지 않음

    # 3) 큐레토리얼 코멘트 생성
    poetic_story = ""
    try:
        prompt = _build_curatorial_prompt(
            persona=aspect,
            text=text,
            tags=tags,
            image_summaries=image_summaries,
        )
        poetic_story = _generate_text_with_retry(prompt)
    except Exception as e:
        st.warning(f"큐레이션 생성 실패 — 기본 문구로 대체합니다: {e}")
        poetic_story = ""

    if not poetic_story:
        poetic_story = FALLBACK_STORY[aspect]

    # 4) quote 폴백
    quote = text or "창가로 들어오는 조용한 빛과 마음이 정돈되던 순간."

    # 5) 결과
    return {
        "persona": aspect,
        "date": datetime.date.today().strftime("%Y.%m.%d"),
        "quote": quote,
        "poetic_story": poetic_story,
        "tags": tags if tags else ["#취향아카이브"],
        "photos": photo_data_urls,
        "image_summaries": image_summaries,
        "likes": 0,
    }


# ------------------------------------------------------------------
# 6. 헬스체크 (배포 직후 확인용)
# ------------------------------------------------------------------
def health_check() -> dict:
    return {
        "has_api_key": "GOOGLE_API_KEY" in st.secrets,
        "model": _get_model_name(),
        "max_images": MAX_IMAGES,
        "max_side": MAX_IMAGE_SIDE,
    }