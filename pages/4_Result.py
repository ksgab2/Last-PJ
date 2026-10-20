import streamlit as st


from Lib.supabase_client import get_supabase

# ... (기존 Result 렌더링 코드) ...

if st.button("SAVE TO SHELVES →", type="primary"):
    result = st.session_state.entry_result
    supabase = get_supabase()

    # dict에서 필요한 컬럼만 골라서 저장
    row = {
        "persona": result["persona"],
        "quote": result["quote"],
        "poetic_story": result["poetic_story"],
        "tags": result["tags"],
        "photos": result["photos"],  # base64 문자열 배열
        "likes": 0,
    }

    try:
        supabase.table("entries").insert(row).execute()
        st.success("서가에 저장되었습니다!")
        st.switch_page("pages/5_Shelves.py")
    except Exception as e:
        st.error(f"저장 실패: {e}")