import streamlit as st
from google import genai

st.set_page_config(page_title="취향 아카이브", page_icon="🧩")
st.title("취향 아카이브")
st.caption("서버 구축 확인용 페이지")

# 1) 시크릿 로드 확인 (키 자체는 절대 출력하지 않음)
has_key = "GOOGLE_API_KEY" in st.secrets
st.write(f"API 키 로드: {'✅' if has_key else '❌'}")

# 2) Gemini 호출 테스트
if has_key and st.button("Gemini 연결 테스트"):
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    resp = client.models.generate_content(
        model="gemini-3.8-flash",
        contents="한 문장으로 자기소개 해줘. 20자 이내.",
    )
    st.success(resp.text)

