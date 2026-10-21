import streamlit as st
from pathlib import Path
import streamlit.components.v1 as components

# 1. 템플릿 로드
TPL = Path(__file__).parent.parent / "templates"
head = (TPL / "head.html").read_text(encoding="utf-8")
body = (TPL / "page2_aspect.html").read_text(encoding="utf-8")

# 2. 현재 선택된 값에 따라 카드를 강조하는 JS
current_aspect = st.session_state.get("aspect", "")
highlight_js = f"""
<script>
document.addEventListener("DOMContentLoaded", () => {{
    const selected = "{current_aspect}";
    if (selected) {{
        const card = document.getElementById('aspect-' + selected);
        if (card) {{
            card.classList.remove('border-transparent');
            card.classList.add('border-archive-dark', 'bg-archive-craft/20');
            const icon = card.querySelector('.check-icon');
            if (icon) icon.className = 'fa-solid fa-circle-check check-icon text-sm text-archive-terracotta';
        }}
    }}
}});
</script>
"""

# 3. HTML 렌더링 (카드 부분만)
html = head.replace("</head>", f"<body>{body}{highlight_js}</body></html>")
components.html(html, height=550, scrolling=False)

# 4. 텍스트와 버튼을 하나의 검은색 영역으로 묶는 CSS 적용
st.markdown("""
<style>
    /* 1. 텍스트가 들어가는 상단 검은색 박스 */
    .dark-selector-box {
        background-color: #2A2825;
        padding: 10px 30px 0px 30px; /* 위쪽은 여백, 아래쪽은 버튼과 붙도록 0 */
        margin-top: -20px; /* iframe과 자연스럽게 이어지도록 */
        text-align: center;
    }
    .dark-selector-box h4 {
        color: #F5F2EC;
        font-family: 'Noto Serif KR', serif;
        margin: 0;
        padding-bottom: 10px;
    }

    /* 2. 버튼 컬럼을 감싸는 영역의 배경을 검은색으로 변경 */
    /* st.columns 바로 위의 stMarkdown 다음에 오는 horizontal block을 타겟팅 */
    div[data-testid="stHorizontalBlock"] {
        background-color: #2A2825;
        padding: 10px 30px 30px 30px;
        margin-top: 0px;
        border-radius: 0px 0px 8px 8px; /* 아래쪽 모서리만 둥글게 */
    }

    /* 3. 버튼 기본 스타일 (검은 배경에 어울리게) */
    div[data-testid="stHorizontalBlock"] button {
        border: 1px solid #6E675F;
        color: #F5F2EC;
        background-color: transparent;
        transition: all 0.3s ease;
    }

    /* 마우스 호버 시 */
    div[data-testid="stHorizontalBlock"] button:hover {
        border-color: #F5F2EC;
        color: #FFFFFF;
        background-color: rgba(245, 242, 236, 0.1);
    }

    /* 선택된 경우 (type="primary") */
    div[data-testid="stHorizontalBlock"] button[kind="primary"] {
        background-color: #9B4028; /* 테라코타 색상 */
        color: #FFFFFF;
        border: 1px solid #9B4028;
    }
</style>

<div class="dark-selector-box">
    <h4>위 카드 중 하나를 선택하세요</h4>
</div>
""", unsafe_allow_html=True)

# 5. 버튼 3개 배치
c1, c2, c3 = st.columns(3)

with c1:
    if st.button("LIA 선택", use_container_width=True, type="primary" if current_aspect == "lia" else "secondary"):
        st.session_state.aspect = "lia"
        st.rerun()

with c2:
    if st.button("OL 선택", use_container_width=True, type="primary" if current_aspect == "ol" else "secondary"):
        st.session_state.aspect = "ol"
        st.rerun()

with c3:
    if st.button("LET 선택", use_container_width=True, type="primary" if current_aspect == "let" else "secondary"):
        st.session_state.aspect = "let"
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# 6. 선택 완료 후 다음 단계로 이동
if current_aspect:
    st.success(f"✅ **{current_aspect.upper()}** 스타일이 선택되었습니다.")

    col_back, col_next = st.columns([1, 2])
    with col_back:
        if st.button("← BACK", use_container_width=True):
            st.switch_page("pages/1_Cover.py")
    with col_next:
        if st.button("NEXT → ENTRY", use_container_width=True, type="primary"):
            st.switch_page("pages/4_Entry.py")  # 파일명에 맞게 수정하세요
else:
    if st.button("← BACK", use_container_width=True):
        st.switch_page("pages/1_Cover.py")