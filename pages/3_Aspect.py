import streamlit as st

# 1. HTML 구조 (기존 디자인 유지)
html_content = """
<div class="aspect-container">
    <div class="header">
        <span class="subtitle">02. EXPRESSIONAL COMPONENT</span>
        <h2>아트워크를 구성할 주요 시선 레이어</h2>
        <p>결과물을 이루는 LIA, OL, LET 중 어떤 조형적 관점에 비중을 둘지 선택합니다.</p>
    </div>

    <div class="cards-wrapper">
        <!-- LIA -->
        <div class="aspect-card" id="lia" data-id="lia">
            <div class="card-visual film-frame">
                <div class="frame-header"><span>FILM #01</span><span>SILHOUETTE</span></div>
                <div class="frame-body"><div class="silhouette-mock"></div></div>
            </div>
            <div class="card-content">
                <div class="title-row"><h3>LIA</h3><span class="role">Text & Silhouette</span></div>
                <p>문장의 잔상과 필름 프레임 속 피사체의 <strong>여백, 실루엣, 텍스트 서사</strong> 중심의 정제된 조형.</p>
            </div>
            <div class="card-footer"><span>#문장잔상 #실루엣</span><span class="check">✓</span></div>
        </div>

        <!-- OL -->
        <div class="aspect-card" id="ol" data-id="ol">
            <div class="card-visual film-frame">
                <div class="frame-header"><span>COLLAGE #02</span><span>TEXTURE</span></div>
                <div class="frame-body"><div class="texture-mock"></div></div>
            </div>
            <div class="card-content">
                <div class="title-row"><h3>OL</h3><span class="role">Visual & Texture</span></div>
                <p>찢어진 수제 종이의 거친 질감, <strong>색면 구도와 시각적 파편</strong>이 만들어내는 명확한 시각성.</p>
            </div>
            <div class="card-footer"><span>#종이질감 #시각파편</span><span class="check">✓</span></div>
        </div>

        <!-- LET -->
        <div class="aspect-card" id="let" data-id="let">
            <div class="card-visual film-frame">
                <div class="frame-header"><span>OVERLAY #03</span><span>SYNTHESIS</span></div>
                <div class="frame-body"><div class="layer-mock">LAYER</div></div>
            </div>
            <div class="card-content">
                <div class="title-row"><h3>LET</h3><span class="role">Synthesis & Layer</span></div>
                <p>필름 네거티브와 텍스트, <strong>다층 오버레이 조화</strong>로 완성되는 차분하고 완성도 높은 융합.</p>
            </div>
            <div class="card-footer"><span>#오버레이 #다층조화</span><span class="check">✓</span></div>
        </div>
    </div>
</div>
"""

# 2. CSS 스타일 (Shadow DOM 내부에서 동작하도록 설계)
css_content = """
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@300;400;600;700&family=Space+Mono&display=swap');

body {
    background-color: #2A2825;
    margin: 0;
    padding: 20px;
    font-family: 'Noto Serif KR', serif;
    color: #F5F2EC;
    box-sizing: border-box;
}
.header { margin-bottom: 30px; }
.header .subtitle { font-family: 'Space Mono', monospace; font-size: 12px; color: #9B4028; letter-spacing: 0.1em; text-transform: uppercase; }
.header h2 { font-size: 28px; margin: 5px 0; }
.header p { font-size: 14px; color: #D3C9B8; margin: 0; }

.cards-wrapper {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    perspective: 1000px;
}

.aspect-card {
    background-color: #F5F2EC;
    padding: 20px;
    border-radius: 4px;
    cursor: pointer;
    position: relative;
    box-shadow: 0 10px 20px rgba(0,0,0,0.3);
    transform-style: preserve-3d;
    transition: opacity 0.4s ease;
    border: 2px solid transparent;
}

.card-visual {
    background-color: #1C1A18;
    padding: 12px;
    margin-bottom: 15px;
    border-radius: 2px;
}
.frame-header { display: flex; justify-content: space-between; font-family: 'Space Mono', monospace; font-size: 9px; color: #6E675F; margin-bottom: 15px; }
.frame-body { height: 100px; display: flex; align-items: center; justify-content: center; position: relative; }

/* 카드 내부 그래픽 목업 */
.silhouette-mock { width: 30px; height: 50px; background: #D3C9B8; border: 1px solid #6E675F; }
.texture-mock { width: 60px; height: 50px; background: #9B4028; opacity: 0.7; transform: rotate(15deg); }
.layer-mock { width: 60px; height: 60px; border: 1px solid #D3C9B8; display: flex; align-items: center; justify-content: center; font-family: 'Space Mono', monospace; font-size: 10px; color: #D3C9B8; }

.card-content { color: #2A2825; }
.title-row { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 8px; }
.title-row h3 { font-size: 20px; margin: 0; }
.title-row .role { font-family: 'Space Mono', monospace; font-size: 10px; color: #9B4028; text-transform: uppercase; }
.card-content p { font-size: 12px; color: #6E675F; line-height: 1.5; margin-bottom: 15px; }

.card-footer { display: flex; justify-content: space-between; font-family: 'Space Mono', monospace; font-size: 10px; color: #6E675F; border-top: 1px solid #D3C9B8; padding-top: 10px; }
.check { opacity: 0; color: #9B4028; font-weight: bold; transition: opacity 0.3s; }

/* 선택된 상태 (Selected) */
.aspect-card.selected { border-color: #9B4028; }
.aspect-card.selected .check { opacity: 1; }
/* 선택되지 않은 상태 (Dimmed) */
.aspect-card.dimmed { opacity: 0.3; transform: scale(0.95); }
"""

# 3. JavaScript (GSAP 애니메이션 및 Python 통신)
js_content = """
export default function(component) {
    const { parentElement, setTriggerValue } = component;
    const data = window.PAGE_DATA || {};
    const currentSelected = data.selected;

    // GSAP 라이브러리 동적 로드
    const script = document.createElement('script');
    script.src = "https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js";
    script.onload = () => {
        initAnimations();
    };
    document.head.appendChild(script);

    function initAnimations() {
        const cards = parentElement.querySelectorAll('.aspect-card');

        // 이전에 선택한 카드가 있으면 상태 복원
        if (currentSelected) {
            cards.forEach(card => {
                if (card.dataset.id === currentSelected) {
                    card.classList.add('selected');
                    gsap.set(card, { scale: 1.05, zIndex: 10 });
                } else {
                    card.classList.add('dimmed');
                }
            });
        }

        cards.forEach(card => {
            // 1. 마우스 호버 애니메이션
            card.addEventListener('mouseenter', () => {
                if (card.classList.contains('dimmed')) return;
                gsap.to(card, { scale: 1.05, y: -10, boxShadow: "0 25px 50px -12px rgba(0,0,0,0.5)", duration: 0.3, ease: "power2.out" });
            });
            card.addEventListener('mouseleave', () => {
                if (card.classList.contains('dimmed')) return;
                const isSelected = card.classList.contains('selected');
                gsap.to(card, { scale: isSelected ? 1.05 : 1, y: 0, boxShadow: isSelected ? "0 10px 20px rgba(0,0,0,0.3)" : "0 10px 20px rgba(0,0,0,0.3)", duration: 0.3, ease: "power2.out" });
            });

            // 2. 클릭 애니메이션 및 Python 전송
            card.addEventListener('click', () => {
                const id = card.dataset.id;

                cards.forEach(c => {
                    if (c === card) {
                        c.classList.add('selected');
                        c.classList.remove('dimmed');
                        gsap.to(c, { scale: 1.05, y: 0, zIndex: 10, duration: 0.5, ease: "back.out(1.5)" });
                    } else {
                        c.classList.remove('selected');
                        c.classList.add('dimmed');
                        gsap.to(c, { scale: 0.95, y: 0, zIndex: 1, duration: 0.5, ease: "power2.out" });
                    }
                });

                // Python으로 클릭한 ID 전송
                setTriggerValue("selected_aspect", id);
            });
        });
    }
}
"""

# 4. 커스텀 컴포넌트 등록
aspect_selector_component = st.components.v2.component(
    name="gsap_aspect_selector",
    html=html_content,
    css=css_content,
    js=js_content,
)

# 5. Python 상태 관리
current = st.session_state.get("aspect")


# 콜백 함수 정의 (JS에서 값이 넘어오면 실행됨)
def on_aspect_change():
    val = st.session_state.gsap_aspect_selector.selected_aspect
    if val and val != st.session_state.get("aspect"):
        st.session_state.aspect = val
        # 상태만 업데이트하고 화면은 그대로 둡니다.


# 컴포넌트 렌더링 (Python 데이터를 JS로 전달)
aspect_selector_component(
    key="gsap_aspect_selector",
    on_selected_aspect_change=on_aspect_change,
    data={"selected": current}
)

# ==========================================
# 6. 하단 UI (선택 후 다음 단계 버튼)
# ==========================================
st.markdown("<br>", unsafe_allow_html=True)

# 컴포넌트의 콜백이 갱신한 세션 상태를 다시 읽어옵니다.
current = st.session_state.get("aspect")

if current:
    st.success(f"✅ **{current.upper()}** 스타일이 선택되었습니다.")

    col_back, col_next = st.columns([1, 2])
    with col_back:
        if st.button("← BACK", use_container_width=True):
            st.switch_page("pages/1_Cover.py")
    with col_next:
        if st.button("NEXT → ENTRY", use_container_width=True, type="primary"):
            st.switch_page("pages/4_Entry.py")
else:
    st.info("💡 위 카드를 직접 클릭하여 스타일을 선택해주세요.")
    if st.button("← BACK", use_container_width=True):
        st.switch_page("pages/1_Cover.py")