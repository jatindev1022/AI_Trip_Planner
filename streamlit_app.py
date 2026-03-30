import streamlit as st
import requests
import os

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="AI Trip Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- BACKEND CONNECTION ---
BASE_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# --- MASTER CSS OVERRIDE ---
# This forces a clean, light professional theme regardless of system dark mode settings.
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ========== GLOBAL RESET ========== */
html, body, [data-testid="stAppViewContainer"], .main, .block-container {
    font-family: 'Inter', sans-serif !important;
    background-color: #FAFAFA !important;
    color: #111827 !important;
}

/* ========== SIDEBAR ========== */
[data-testid="stSidebar"] {
    background-color: #FFFFFF !important;
    border-right: 1px solid #E5E7EB !important;
}
[data-testid="stSidebar"] * {
    color: #374151 !important;
}
.sidebar-logo {
    font-size: 1.3rem;
    font-weight: 700;
    color: #111827 !important;
    letter-spacing: -0.5px;
}
.sidebar-tagline {
    font-size: 0.75rem;
    color: #9CA3AF !important;
    margin-top: 4px;
}
.sidebar-section-title {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #9CA3AF !important;
    margin: 16px 0 8px 0;
}
.tech-pill {
    display: inline-block;
    background-color: #F3F4F6;
    color: #374151 !important;
    border: 1px solid #E5E7EB;
    border-radius: 20px;
    padding: 3px 10px;
    font-size: 0.73rem;
    margin: 3px 2px;
}

/* ========== MAIN CONTENT ========== */
.hero-badge {
    display: inline-block;
    background-color: #EFF6FF;
    color: #2563EB;
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.75rem;
    font-weight: 500;
    letter-spacing: 0.04em;
    margin-bottom: 12px;
    border: 1px solid #BFDBFE;
}
.hero-title {
    font-size: 2.2rem;
    font-weight: 700;
    color: #111827;
    letter-spacing: -0.03em;
    line-height: 1.2;
    margin: 0 0 8px 0;
}
.hero-subtitle {
    font-size: 1rem;
    color: #6B7280;
    font-weight: 400;
    margin: 0 0 24px 0;
    line-height: 1.5;
}
.divider {
    border: none;
    border-top: 1px solid #F3F4F6;
    margin: 24px 0;
}

/* ========== SEARCH FORM ========== */
.suggestion-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: #6B7280;
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
.stTextInput > div > div > input {
    background-color: #FFFFFF !important;
    border: 1.5px solid #E5E7EB !important;
    border-radius: 10px !important;
    color: #111827 !important;
    font-size: 0.95rem !important;
    padding: 12px 16px !important;
    font-family: 'Inter', sans-serif !important;
}
.stTextInput > div > div > input:focus {
    border-color: #2563EB !important;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
}
.stTextInput > div > div > input::placeholder {
    color: #9CA3AF !important;
}

/* ========== BUTTONS ========== */
.stButton > button {
    background-color: #111827 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    padding: 10px 18px !important;
    transition: all 0.15s ease !important;
    letter-spacing: 0.01em;
}
.stButton > button:hover {
    background-color: #1F2937 !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
}

/* Quick Select Chips */
.chip-btn > button {
    background-color: #FFFFFF !important;
    color: #374151 !important;
    border: 1.5px solid #E5E7EB !important;
    font-size: 0.8rem !important;
    font-weight: 400 !important;
    border-radius: 20px !important;
    padding: 6px 14px !important;
}
.chip-btn > button:hover {
    border-color: #2563EB !important;
    color: #2563EB !important;
    background-color: #EFF6FF !important;
    transform: none;
    box-shadow: none !important;
}

/* ========== RESULT CARD ========== */
.result-wrapper {
    background-color: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 12px;
    padding: 28px 32px;
    margin-top: 20px;
    color: #1F2937 !important;
    line-height: 1.75;
    font-size: 0.92rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05), 0 1px 2px rgba(0,0,0,0.03);
}
.result-wrapper h1, .result-wrapper h2, .result-wrapper h3 {
    color: #111827 !important;
    font-weight: 600;
    margin-top: 1.5em;
}
.result-wrapper p {
    color: #374151 !important;
}

/* ========== SUCCESS / ERROR STATES ========== */
.stSuccess, .stInfo {
    background-color: #F0FDF4 !important;
    color: #166534 !important;
    border: 1px solid #BBF7D0 !important;
    border-radius: 8px !important;
}
.stSpinner > div {
    color: #2563EB !important;
}

/* ========== EXPANDER ========== */
.streamlit-expanderHeader {
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    color: #6B7280 !important;
    background-color: #FAFAFA !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-logo">✈️ AI Trip Planner</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-tagline">Agentic Itinerary System · v2.0</div>', unsafe_allow_html=True)
    
    st.markdown("---")

    st.markdown('<div class="sidebar-section-title">Developer</div>', unsafe_allow_html=True)
    st.markdown("**Jatin**  \nFull-Stack AI Engineer")
    st.markdown("[GitHub ↗](https://github.com/jatindev1022)   [LinkedIn ↗](https://www.linkedin.com/in/jatin-dev)")

    st.markdown('<div class="sidebar-section-title">Tech Stack</div>', unsafe_allow_html=True)
    st.markdown("""
    <span class="tech-pill">FastAPI</span>
    <span class="tech-pill">LangGraph</span>
    <span class="tech-pill">Llama 3.1</span>
    <span class="tech-pill">Groq</span>
    <span class="tech-pill">Docker</span>
    <span class="tech-pill">Render</span>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-title">How it works</div>', unsafe_allow_html=True)
    with st.expander("View Details"):
        st.markdown("""
        1. Query sent to **FastAPI** backend
        2. **LangGraph** orchestrates tool calls
        3. Agent fetches weather, places, costs
        4. Generates comprehensive itinerary
        """)


# ─────────────────────────────────────────────
# MAIN PAGE
# ─────────────────────────────────────────────
_, col, _ = st.columns([0.08, 1, 0.08])

with col:
    st.markdown('<div class="hero-badge">🤖 Powered by LangGraph + Groq</div>', unsafe_allow_html=True)
    st.markdown('<h1 class="hero-title">Plan your next trip  <br>with AI.</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Describe where you want to go. The agent will research weather,<br>attractions, costs, and build a complete itinerary for you.</p>', unsafe_allow_html=True)

    # Quick suggestions
    st.markdown('<div class="suggestion-label">Quick suggestions</div>', unsafe_allow_html=True)
    chip_cols = st.columns([1, 1, 1, 3])
    
    with chip_cols[0]:
        st.markdown('<div class="chip-btn">', unsafe_allow_html=True)
        if st.button("Paris"):
            st.session_state["q"] = "Plan a 3-day romantic trip to Paris."
        st.markdown('</div>', unsafe_allow_html=True)
    with chip_cols[1]:
        st.markdown('<div class="chip-btn">', unsafe_allow_html=True)
        if st.button("Bali"):
            st.session_state["q"] = "7-day relaxation trip in Bali, Indonesia."
        st.markdown('</div>', unsafe_allow_html=True)
    with chip_cols[2]:
        st.markdown('<div class="chip-btn">', unsafe_allow_html=True)
        if st.button("Tokyo"):
            st.session_state["q"] = "5-day cultural food trip in Tokyo."
        st.markdown('</div>', unsafe_allow_html=True)

    # Input Form
    with st.form(key="travel_form"):
        user_input = st.text_input(
            label="",
            value=st.session_state.get("q", ""),
            placeholder="e.g., A 5-day budget trip to Manali for two people..."
        )
        submit_button = st.form_submit_button(label="Generate Itinerary →")

    # Result
    if submit_button and user_input.strip():
        try:
            with st.spinner("Agent is researching your destination..."):
                payload = {"question": user_input}
                response = requests.post(f"{BASE_URL}/query", json=payload, timeout=180)
            
            if response.status_code == 200:
                answer = response.json().get("answer", "No response returned.")
                st.markdown(f'<div class="result-wrapper">{answer}</div>', unsafe_allow_html=True)
                st.markdown("")
                st.caption("✓ Plan generated by AI. Verify prices and availability before booking.")
            else:
                err = response.json().get("error", response.text)
                st.error(f"Backend Error: {err}")
        except Exception as e:
            st.error(f"Could not connect to backend at `{BASE_URL}`.")
            st.info("If using the free Render tier, wait 30–45 seconds for the server to wake up and try again.")