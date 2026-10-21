import streamlit as st

# 빈티지 도록 스타일을 위한 CSS
st.markdown("""
<style>
    .consent-title { font-family: 'Noto Serif KR', serif; font-size: 28px; font-weight: bold; margin-bottom: 10px; color: #2A2825; }
    .consent-sub { font-size: 11px; color: #9B4028; letter-spacing: 0.1em; margin-bottom: 5px; font-family: monospace; }
    .consent-desc { font-size: 13px; color: #6E675F; margin-bottom: 25px; line-height: 1.6; }
    .notice-box { background-color: #F5F2EC; border-left: 4px solid #9B4028; padding: 15px; font-size: 12px; color: #2A2825; margin-bottom: 20px; line-height: 1.6; }
    .all-agree-box { background-color: #EAE5DC; padding: 15px; border-radius: 4px; margin-bottom: 20px; border: 1px solid #D3C9B8; }
    .item-title { font-weight: bold; font-size: 14px; color: #2A2825; }
    .item-sub { font-size: 11px; color: #6E675F; margin-top: 2px; }
    .ai-notice { background-color: #F5F2EC; padding: 20px; border-radius: 4px; font-size: 12px; color: #2A2825; line-height: 1.6; margin-top: 30px; border: 1px solid #D3C9B8; }
</style>
""", unsafe_allow_html=True)

# ----------------- 1. 헤더 -----------------
st.markdown('<div class="consent-sub">BEFORE CREATING YOUR ARCHIVE</div>', unsafe_allow_html=True)
st.markdown('<div class="consent-title">작품 제작을 위한 동의</div>', unsafe_allow_html=True)
st.markdown('<div class="consent-desc">LIAOLLET은 업로드된 사진과 글을 바탕으로 AI 콜라주 작품을 만듭니다. 선택 항목에 동의하지 않아도 작품을 생성하고 다운로드할 수 있습니다.</div>', unsafe_allow_html=True)

# ----------------- 2. 안내 문구 -----------------
st.markdown('<div class="notice-box">검토용 시안입니다. 실제 운영주체·보관기간·연락처 등 [대괄호] 항목이 확정되기 전에는 공개용으로 사용할 수 없습니다.</div>', unsafe_allow_html=True)

# ----------------- 3. 전체 동의 체크박스 로직 -----------------
# 세션 상태 초기화
if "consent_req1" not in st.session_state: st.session_state.consent_req1 = False
if "consent_req2" not in st.session_state: st.session_state.consent_req2 = False
if "consent_opt1" not in st.session_state: st.session_state.consent_opt1 = False
if "consent_opt2" not in st.session_state: st.session_state.consent_opt2 = False

def toggle_all():
    val = st.session_state.consent_all
    st.session_state.consent_req1 = val
    st.session_state.consent_req2 = val
    st.session_state.consent_opt1 = val
    st.session_state.consent_opt2 = val

st.markdown('<div class="all-agree-box">', unsafe_allow_html=True)
st.checkbox("전체 동의하기", key="consent_all", on_change=toggle_all, help="필수 및 선택 항목 전체에 동의합니다. 선택 동의는 언제든 개별적으로 해제하실 수 있습니다.")
st.markdown('</div>', unsafe_allow_html=True)

# ----------------- 4. 개별 동의 항목 -----------------
st.markdown("---")

col1, col2 = st.columns([8, 2])
with col1:
    st.checkbox("[필수] 개인정보 수집·이용 동의", key="consent_req1")
    st.markdown('<div class="item-sub">사진·문장·선택 스타일을 작품 제작 및 결과 제공에 이용합니다.</div>', unsafe_allow_html=True)
with col2:
    st.caption("[자세히 보기 ▾]")

st.markdown("<br>", unsafe_allow_html=True)

col3, col4 = st.columns([8, 2])
with col3:
    st.checkbox("[필수] 제작물 이용·편집 허락", key="consent_req2")
    st.markdown('<div class="item-sub">제출한 사진·글을 AI 콜라주 제작에 필요한 범위에서 편집·합성합니다.</div>', unsafe_allow_html=True)
with col4:
    st.caption("[자세히 보기 ▾]")

st.markdown("<br>", unsafe_allow_html=True)

col5, col6 = st.columns([8, 2])
with col5:
    st.checkbox("[선택] 완성 작품 갤러리 공개", key="consent_opt1")
    st.markdown('<div class="item-sub">공개에 동의한 완성작만 웹 갤러리에 게시합니다.</div>', unsafe_allow_html=True)
with col6:
    st.caption("[자세히 보기 ▾]")

st.markdown("<br>", unsafe_allow_html=True)

col7, col8 = st.columns([8, 2])
with col7:
    st.checkbox("[선택] 전시 기록·SNS·포토폴리오 활용", key="consent_opt2")
    st.markdown('<div class="item-sub">공식 전시 기록과 홍보에 선택 작품을 활용합니다.</div>', unsafe_allow_html=True)
with col8:
    st.caption("[자세히 보기 ▾]")

# ----------------- 5. AI 안내 문구 -----------------
st.markdown("""
<div class="ai-notice">
    <strong>생성형 AI 이용 안내</strong><br>
    사진과 글을 AI 기술로 재구성하며 결과는 원본과 다를 수 있습니다. 실제 공개 서비스에서는 생성형 AI가 사용되었다는 사실과 AI 생성 결과 표시를 반영합니다.
</div>
""", unsafe_allow_html=True)

# ----------------- 6. 다음 단계 이동 버튼 -----------------
st.markdown("<br><br>", unsafe_allow_html=True)

# 필수 항목 2개가 모두 체크되어야만 버튼 활성화
is_valid = st.session_state.consent_req1 and st.session_state.consent_req2

c1, c2 = st.columns([1, 2])
with c1:
    if st.button("← BACK", use_container_width=True):
        st.switch_page("pages/1_Cover.py")
with c2:
    if st.button("동의하고 시작하기 →", type="primary", use_container_width=True, disabled=not is_valid):
        # 동의 여부를 세션에 최종 저장 (필요시 다른 페이지에서 활용)
        st.session_state.consent_given = True
        st.session_state.gallery_public = st.session_state.consent_opt1
        st.session_state.sns_use = st.session_state.consent_opt2
        st.switch_page("pages/3_Aspect.py")