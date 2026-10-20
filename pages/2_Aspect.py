import streamlit as st


from Lib.render import render_page

st.set_page_config(layout="wide")
render_page("page2_aspect", height=760)   # 카드는 "보여주기"용

st.markdown("#### 주축이 될 표현 레이어를 선택하세요")
choice = st.radio(
    "aspect", ["lia", "ol", "let"],
    format_func=lambda x: {"lia":"LIA — Text & Silhouette",
                           "ol":"OL — Visual & Texture",
                           "let":"LET — Synthesis & Layer"}[x],
    horizontal=True, label_visibility="collapsed",
)

col1, col2 = st.columns([1, 2])
with col1:
    if st.button("← BACK", use_container_width=True):
        st.switch_page("pages/1_Cover.py")
with col2:
    if st.button("NEXT →", use_container_width=True, type="primary"):
        st.session_state.aspect = choice
        st.switch_page("pages/3_Entry.py")