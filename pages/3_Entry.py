import streamlit as st


from Lib.pipeline import analyze_entry

st.set_page_config(layout="wide")
st.markdown("""
<style>
  .block-container { max-width: 780px; background:#F5F2EC; padding:2.5rem; }
  h2 { font-family:'Noto Serif KR', serif; }
</style>
""", unsafe_allow_html=True)

st.markdown("### 기록 도록: 감각과 소스 수집")
st.caption("콜라주에 사용될 사진 파편과 마음속 문장을 담백하게 올려주세요.")

with st.form("entry"):
    files = st.file_uploader("SOURCE 01. 이미지 조각 (최대 5장)",
                             type=["jpg","jpeg","png"],
                             accept_multiple_files=True)
    text = st.text_area("SOURCE 02. 스쳐간 글귀",
                        placeholder="창밖으로 스며들던 빗소리와 차분한 공간의 온도…",
                        height=120)
    tags = st.multiselect("SOURCE 03. 취향 키워드",
        ["#정제된침묵","#흑백필름","#수제종이질감","#건축스케치","#은은한빛"])
    go = st.form_submit_button("GENERATE CATALOGUE →", type="primary",
                               use_container_width=True)

if go:
    if not files and not text:
        st.warning("사진 또는 문장 중 최소 하나는 필요합니다.")
    else:
        with st.spinner("YOLO + Gemini 분석 중…"):
            result = analyze_entry(
                files=files,
                text=text,
                tags=tags,
                aspect=st.session_state.get("aspect", "lia"),
            )
        st.session_state.entry_result = result
        st.switch_page("pages/4_Result.py")