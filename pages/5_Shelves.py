import streamlit as st

from Lib.render import render_page

archive = st.session_state.get("archive", [])
render_page("page5_shelves", data={"items": archive}, height=1200)

if st.button("+ NEW ARCHIVE ENTRY", use_container_width=True):
    st.switch_page("pages/1_Cover.py")