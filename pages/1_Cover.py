import streamlit as st
from Lib.render import render_page

st.set_page_config(layout="wide", page_title="liaollet", page_icon="🧩")
render_page("page1_cover", height=780)

_, col, _ = st.columns([1, 1.2, 1])
with col:
    if st.button("ENTER ARCHIVE →", use_container_width=True, type="primary"):
        st.switch_page("pages/2_Aspect.py")