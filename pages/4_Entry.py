import streamlit as st

from Lib.pipeline import analyze_entry, extract_keywords

st.markdown("### 기록 도록: 감각과 소스 수집")

# 1. 사진 업로드 (최대 3장)
files = st.file_uploader("SOURCE 01. 이미지 조각 (최대 3장)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# 2. 업로드된 사진 3칸 그리드로 보여주기
if files:
    files = files[:3]  # 3장으로 제한
    cols = st.columns(3)
    for i, file in enumerate(files):
        with cols[i]:
            st.image(file, use_container_width=True, caption=f"CUT #{i+1}")

# 3. 글귀 입력
text = st.text_area("SOURCE 02. 스쳐간 글귀", height=120)

# 4. AI 키워드 추출 및 선택
st.markdown("**SOURCE 03. 취향 키워드**")
if st.button("✨ AI에게 키워드 추천받기"):
    if not files and not text:
        st.warning("사진이나 글귀를 먼저 입력해주세요.")
    else:
        with st.spinner("이미지와 글귀를 분석해 키워드를 추출 중…"):
            # extract_keywords 함수가 사진과 글귀를 분석해 #키워드 리스트 반환
            extracted = extract_keywords(files, text)
            st.session_state.ai_keywords = extracted

# 추출된 키워드가 있으면 multiselect로 선택하게 함
default_tags = st.session_state.get("ai_keywords", ["#정제된침묵", "#흑백필름", "#수제종이질감"])
selected_tags = st.multiselect("추출된 키워드 중 사용할 것을 선택하세요 (수정 가능)",
                               options=list(set(default_tags + ["#은은한빛", "#건축스케치", "#여름바이브", "#몽환적", "#원색"])),
                               default=default_tags)

st.markdown("---")
if st.button("GENERATE CATALOGUE →", type="primary", use_container_width=True):
    if not files and not text:
        st.warning("사진 또는 문장 중 최소 하나는 필요합니다.")
    else:
        # analyze_entry 호출 (병렬 처리)
        result = analyze_entry(
            files=files, text=text, tags=selected_tags, aspect=st.session_state.get("aspect", "lia")
        )
        st.session_state.entry_result = result
        st.switch_page("pages/4_Result.py")