import streamlit as st

from Lib.render import render_page

if "entry_result" not in st.session_state:
    st.warning("먼저 Entry에서 분석을 실행하세요.")
    st.stop()

r = st.session_state.entry_result
render_page("page4_result", data=r, height=1100)

c1, c2 = st.columns(2)
with c1:
    if st.button("← BACK", use_container_width=True):
        st.switch_page("pages/3_Entry.py")
with c2:
    if st.button("SAVE TO SHELVES →", use_container_width=True, type="primary"):
        st.session_state.setdefault("archive", []).append(r)
        st.switch_page("pages/5_Shelves.py")