import streamlit as st

from Lib.render import render_page
from Lib.supabase_client import get_supabase

# 결과 화면을 넓게 쓰기 위한 설정 (필요시 app.py에 있어도 됨)
#st.set_page_config(layout="wide")

if "entry_result" not in st.session_state:
    st.warning("먼저 Entry에서 분석을 실행하세요.")
    st.stop()

result = st.session_state.entry_result

# ==========================================
# 1. 결과 화면을 크게 표시 (높이를 1400으로 확장)
# ==========================================
render_page("page4_result", data=result, height=1400)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 이 아카이브를 어떻게 할까요?")
st.caption("결과를 확인한 뒤, 마음에 들면 서가에 저장하고 아니면 돌아가서 다시 만들어보세요.")

# ==========================================
# 2. 저장 여부 결정 버튼 (좌우로 크게 배치)
# ==========================================
col1, col2 = st.columns(2)

with col1:
    if st.button("❌ 저장하지 않고 돌아가기 (폐기)", use_container_width=True):
        # 임시 결과 삭제 (잘못 저장되는 것 방지)
        del st.session_state["entry_result"]
        st.switch_page("pages/3_Entry.py")

with col2:
    if st.button("✅ 서가에 저장하기 (SAVE)", use_container_width=True, type="primary"):
        supabase = get_supabase()

        row = {
            "persona": result["persona"],
            "quote": result["quote"],
            "poetic_story": result["poetic_story"],
            "tags": result["tags"],
            "photos": result["photos"],
            "likes": 0,
        }

        try:
            supabase.table("entries").insert(row).execute()
            st.success("서가에 성공적으로 저장되었습니다!")
            # 저장 후 임시 결과 삭제
            del st.session_state["entry_result"]
            st.switch_page("pages/5_Shelves.py")
        except Exception as e:
            st.error(f"저장 실패: {e}")