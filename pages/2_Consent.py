import streamlit as st
import datetime

# 1. 전역 CSS 스타일 (액자 및 종이 효과)
st.markdown("""
<style>
 
    
    
    
    /* 1. 가장 바깥쪽 배경 (아주 어두운 갈색) */
    .stApp {
        background-color: #1A1816 !important;
    }

    /* 2. 중앙 레이아웃 여백 조정 */
    .block-container {
        padding-top: 4rem !important;
        padding-bottom: 4rem !important;
    }

    /* 3. 가운데 열을 '갈색 액자 + 종이'로 만들기 */
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) {
        background-color: #F5F2EC !important; /* 종이 색상 */
        border: 24px solid #2A2825; /* 갈색 액자 테두리 */
        border-radius: 24px; /* 둥근 모서리 */
        padding: 40px 30px !important;
        box-shadow: 0 20px 50px rgba(0,0,0,0.8); /* 입체감 */
        position: relative;
        max-width: 500px;
        margin: 0 auto;
    }

    /* 4. 상단 테이프 효과 (액자 위에 붙임) */
    div[data-testid="stHorizontalBlock"] > div:nth-child(2)::before {
        content: "";
        position: absolute;
        top: -38px; /* 액자 테두리 두께만큼 위로 올림 */
        left: 40px;
        width: 80px;
        height: 24px;
        background-color: rgba(211, 201, 184, 0.85);
        transform: rotate(-3deg);
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        z-index: 10;
    }

    /* 5. 텍스트 및 체크박스 디자인 */
    .page-num { text-align: right; font-family: 'Space Mono', monospace; font-size: 12px; color: #6E675F; margin-bottom: 10px; }
    .paper-title { font-size: 32px; font-weight: 800; color: #2A2825; margin-bottom: 5px; font-family: 'Noto Serif KR', serif; }
    .paper-sub { font-size: 16px; color: #6E675F; margin-bottom: 30px; font-family: 'Nanum Brush Script', serif;font-weight: bold; }

    /* 체크박스 라벨 색상 */
    div[data-testid="stCheckbox"] label p {
        color: #2A2825 !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        line-height: 1.4 !important;
    }
    /* 체크박스 네모 모양으로 변경 */
    div[data-testid="stCheckbox"] div[role="checkbox"] {
        border-radius: 0px !important;
        border: 2px solid #2A2825 !important;
        width: 22px !important;
        height: 22px !important;
    }
    div[data-testid="stCheckbox"] div[role="checkbox"][aria-checked="true"] {
        background-color: transparent !important;
        border-color: #2A2825 !important;
    }
    div[data-testid="stCheckbox"] svg {
        fill: #2A2825 !important;
        width: 16px !important;
        height: 16px !important;
    }

    /* 스탬프 */
    .stamp {
        border: 2px solid #B5473A;
        border-radius: 50%;
        color: #B5473A;
        width: 100px;
        height: 100px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        transform: rotate(-10deg);
        font-family: 'Space Mono', monospace;
        font-size: 10px;
        text-align: center;
        opacity: 0.8;
        margin: 0 auto;
    }
    
</style>
""", unsafe_allow_html=True)

# 2. 3열 레이아웃 생성 (가운데 열이 액자 역할)
col_left, col_paper, col_right = st.columns([1, 2, 1])

with col_paper:
    # 종이 위의 타이틀
    st.markdown("""
    <div class="page-num">p.02 / 07</div>
    <div class="paper-title">입장 동의서</div>
    <div class="paper-sub">다락방에 들어가기 전, 작은 약속</div>
    """, unsafe_allow_html=True)

    # 세션 상태 초기화
    if "c1" not in st.session_state: st.session_state.c1 = False
    if "c2" not in st.session_state: st.session_state.c2 = False
    if "c3" not in st.session_state: st.session_state.c3 = False


    def agree_all():
        st.session_state.c1 = True
        st.session_state.c2 = True
        st.session_state.c3 = True


    # 체크박스들
    st.checkbox("업로드한 사진과 문장은 작품 생성에만 사용됩니다.", key="c1")

    st.checkbox("사진 속 인물이 작품에 반영될 수 있습니다.", key="c2")
    # 서브 텍스트
    st.markdown(
        "<div style='margin-left: 32px; margin-top: -15px; margin-bottom: 20px; font-size: 12px; color: #6E675F; font-family: \"Noto Serif KR\";'>타인의 동의 없는 사진은 올리지 말아 주세요.</div>",
        unsafe_allow_html=True)

    st.checkbox("완성된 작품이 익명으로 '취향의 서가'에 전시·활용되는 것에 동의합니다.", key="c3")

    st.markdown("<br>", unsafe_allow_html=True)

    # 모두 동의 버튼과 스탬프
    c_btn, c_stamp = st.columns([1, 1])
    with c_btn:
        st.button("모두 동의", use_container_width=True, on_click=agree_all)
    with c_stamp:
        if st.session_state.c1 and st.session_state.c2 and st.session_state.c3:
            today = datetime.date.today().strftime("%Y.%m.%d")
            st.markdown(f"""
            <div class="stamp">
                <div style="font-size: 12px; font-weight: bold; margin-bottom: 2px;">LIAOLLET</div>
                <div>AGREED</div>
                <div>{today}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # 이전 / 다음 버튼
    b1, b2 = st.columns(2)
    with b1:
        if st.button("← 이전", use_container_width=True):
            st.switch_page("pages/1_Cover.py")
    with b2:
        is_valid = st.session_state.c1 and st.session_state.c3
        if st.button("다음 장 →", type="primary", use_container_width=True, disabled=not is_valid):
            st.session_state.consent_given = True
            st.session_state.gallery_public = st.session_state.c3
            st.switch_page("pages/3_Aspect.py")