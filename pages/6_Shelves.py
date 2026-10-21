import streamlit as st
from Lib.render import render_page
from Lib.supabase_client import get_supabase

supabase = get_supabase()

# 최신순으로 모든 아카이브 가져오기
try:
    response = (
        supabase.table("entries")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )
    items = response.data
except Exception as e:
    st.error(f"불러오기 실패: {e}")
    items = []

render_page("page5_shelves", data={"items": items}, height=1400)