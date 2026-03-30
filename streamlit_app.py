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

BASE_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# --- LIGHT THEME CSS ONLY ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif !important; }

/* All buttons - clean light style */
div.stButton > button,
div.stFormSubmitButton > button {
    background-color: #F3F4F6 !important;
    color: #111827 !important;
    border: 1px solid #D1D5DB !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    padding: 0.5rem 1.2rem !important;
    transition: all 0.15s ease !important;
    width: 100% !important;
}
div.stButton > button:hover,
div.stFormSubmitButton > button:hover {
    background-color: #E5E7EB !important;
    border-color: #9CA3AF !important;
}

/* Generate button - slightly more prominent */
div.stFormSubmitButton > button {
    background-color: #FFFFFF !important;
    border: 1.5px solid #9CA3AF !important;
    width: auto !important;
    font-weight: 600 !important;
}

/* Text input */
.stTextInput > div > div > input {
    background-color: #FFFFFF !important;
    border: 1.5px solid #D1D5DB !important;
    border-radius: 8px !important;
    color: #111827 !important;
    font-size: 0.92rem !important;
    padding: 0.65rem 1rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #9CA3AF !important;
    box-shadow: 0 0 0 2px rgba(0,0,0,0.05) !important;
}
.stTextInput > div > div > input::placeholder {
    color: #9CA3AF !important;
}
label[data-testid="stWidgetLabel"] { display: none !important; }

/* Result card */
.result-card {
    background-color: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 12px;
    padding: 28px 32px;
    line-height: 1.8;
    color: #374151;
    font-size: 0.9rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    margin-top: 8px;
}
.result-card h1, .result-card h2, .result-card h3 {
    color: #111827;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ✈️ AI Trip Planner")
    st.caption("Agentic Itinerary System · v2.0")
    st.divider()

    st.markdown("**Developer**")
    st.markdown("Jatin — Full-Stack AI Engineer")
    st.markdown("[GitHub](https://github.com/jatindev1022) · [LinkedIn](https://www.linkedin.com/in/jatin-dev)")

    st.divider()

    st.markdown("**Tech Stack**")
    st.markdown("""
    - FastAPI (Backend)
    - LangGraph (Agentic Logic)
    - Llama 3.1-70B via Groq
    - Docker + Render (Infra)
    """)

    st.divider()

    with st.expander("How it works"):
        st.markdown("""
        1. Your query hits the FastAPI backend.
        2. LangGraph coordinates agent tools.
        3. Agent fetches weather, places, costs.
        4. Returns a full itinerary in Markdown.
        """)


# ─────────────────────────────────────────────
# MAIN CONTENT
# ─────────────────────────────────────────────
st.markdown("""
<h1 style="font-size:2rem; font-weight:700; color:#111827; letter-spacing:-0.03em; margin-bottom:6px;">
Plan your next trip with AI.
</h1>
<p style="color:#6B7280; font-size:0.95rem; margin-bottom:24px; line-height:1.6;">
Describe your destination. The agent researches weather, places, and costs — then builds a full itinerary.
</p>
""", unsafe_allow_html=True)

# Quick Suggestions
st.markdown('<p style="font-size:0.72rem; font-weight:600; color:#9CA3AF; letter-spacing:0.08em; margin-bottom:6px;">QUICK SUGGESTIONS</p>', unsafe_allow_html=True)

c1, c2, c3, _ = st.columns([1, 1, 1, 4])
with c1:
    if st.button("Paris"):
        st.session_state["q"] = "Plan a 3-day romantic trip to Paris, France."
with c2:
    if st.button("Bali"):
        st.session_state["q"] = "A relaxing 7-day trip in Bali, Indonesia."
with c3:
    if st.button("Tokyo"):
        st.session_state["q"] = "A 5-day cultural food trip in Tokyo, Japan."

st.markdown("")

# Search Form
with st.form(key="trip_form"):
    user_input = st.text_input(
        label="destination",
        value=st.session_state.get("q", ""),
        placeholder="e.g., A 5-day budget trip to Manali for two people..."
    )
    _, btn_col = st.columns([4, 1])
    with btn_col:
        submitted = st.form_submit_button("Generate →")

# ─────────────────────────────────────────────
# RESULT
# ─────────────────────────────────────────────
if submitted and user_input.strip():
    try:
        with st.spinner("Researching your destination..."):
            res = requests.post(f"{BASE_URL}/query", json={"question": user_input}, timeout=180)

        if res.status_code == 200:
            answer = res.json().get("answer", "No itinerary returned.")
            st.markdown(f'<div class="result-card">{answer}</div>', unsafe_allow_html=True)
            st.caption("✓ AI-generated plan. Please verify details before booking.")
        else:
            err = res.json().get("error", res.text)
            st.error(f"Backend error: {err}")

    except Exception as e:
        st.error(f"Could not reach backend at `{BASE_URL}`.")
        st.info("On the free Render tier, the server sleeps after inactivity. Wait 30–45s and try again.")