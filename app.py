import streamlit as st

st.set_page_config(
    layout="wide",
    page_title="liaollet",
    page_icon="🧩"
)

pg = st.navigation([
    st.Page("pages/1_Cover.py", title="01.COVER", default=True),
    st.Page("pages/2_Consent.py", title="02.CONSENT"),  # ← 신규 추가
    st.Page("pages/3_Aspect.py", title="03.ASPECT"),
    st.Page("pages/4_Entry.py", title="04.ENTRY"),
    st.Page("pages/5_Result.py", title="05.ARTWORK"),
    st.Page("pages/6_Shelves.py", title="06.SHELVES"),
])
pg.run()