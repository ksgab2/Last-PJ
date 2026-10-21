import streamlit as st
import random


from Lib.render import render_page

# 세션에 티켓 번호가 없으면 생성
if "ticket_no" not in st.session_state:
    st.session_state.ticket_no = f"{random.randint(1, 500):03d}"

render_page("page1_cover", data={"ticket_no": st.session_state.ticket_no}, height=780)

_, col, _ = st.columns([1, 1.2, 1])
with col:
    if st.button("ENTER ARCHIVE →", use_container_width=True, type="primary"):
        st.switch_page("pages/2_Consent.py")  # ← 경로 변경