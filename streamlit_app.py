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

# --- GLOBAL CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Force Light Theme */
:root {
    --background: #ffffff;
    --surface: #f9fafb;
    --border: #e5e7eb;
    --text-primary: #111827;
    --text-secondary: #6b7280;
    --accent: #2563eb;
    --accent-light: #eff6ff;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--background) !important;
    font-family: 'Inter', sans-serif !important;
    color: var(--text-primary) !important;
}
.main .block-container {
    background-color: var(--background) !important;
    padding-top: 2.5rem !important;
    padding-bottom: 3rem !important;
    max-width: 800px !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #FAFAFA !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
}

/* All buttons - default style (Generate Itinerary) */
div.stButton > button {
    background-color: #111827 !important;
    color: #ffffff !important;
    border: 1.5px solid #111827 !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.875rem !important;
    padding: 0.55rem 1.25rem !important;
    transition: background-color 0.15s, border-color 0.15s !important;
    width: 100%;
}
div.stButton > button:hover {
    background-color: #1f2937 !important;
    border-color: #1f2937 !important;
}

/* Chip buttons override (uses a container class to target them specifically) */
.chip-wrp div.stButton > button {
    background-color: #ffffff !important;
    color: #374151 !important;
    border: 1.5px solid #d1d5db !important;
    border-radius: 100px !important;
    font-size: 0.8rem !important;
    font-weight: 400 !important;
    padding: 0.35rem 1rem !important;
    width: auto !important;
    white-space: nowrap;
}
.chip-wrp div.stButton > button:hover {
    background-color: #eff6ff !important;
    color: #2563eb !important;
    border-color: #2563eb !important;
}

/* Submit button inside form */
div.stFormSubmitButton > button {
    background-color: #111827 !important;
    color: #ffffff !important;
    border: 1.5px solid #111827 !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.875rem !important;
    padding: 0.55rem 1.4rem !important;
    width: auto !important;
}
div.stFormSubmitButton > button:hover {
    background-color: #1f2937 !important;
}

/* Input */
.stTextInput > div > div > input {
    background-color: #ffffff !important;
    border: 1.5px solid #d1d5db !important;
    border-radius: 10px !important;
    color: #111827 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.925rem !important;
    padding: 0.7rem 1rem !important;
    box-shadow: none !important;
}
.stTextInput > div > div > input:focus {
    border-color: #2563eb !important;
    outline: none !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.1) !important;
}
.stTextInput > div > div > input::placeholder {
    color: #9ca3af !important;
}
label[data-testid="stWidgetLabel"] {
    display: none !important;
}

/* Result card */
.result-card {
    background-color: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 28px 32px;
    line-height: 1.8;
    color: #1f2937;
    font-size: 0.9rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    margin-top: 8px;
}
.result-card h1, .result-card h2, .result-card h3 {
    color: #111827;
    font-weight: 600;
}

/* Divider */
.hr { border: none; border-top: 1px solid #f3f4f6; margin: 20px 0; }

/* Caption text */
.caption-text {
    font-size: 0.75rem;
    color: #9ca3af;
    margin-top: 10px;
}

/* Spinner */
[data-testid="stSpinner"] { color: #2563eb !important; }

/* Expander */
[data-testid="stExpander"] summary {
    font-size: 0.78rem !important;
    color: #6b7280 !important;
    font-weight: 500 !important;
}

/* Remove red Streamlit toolbar  */
[data-testid="stToolbar"] { display: none; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ✈️ AI Trip Planner")
    st.caption("Agentic Itinerary System · v2.0")
    st.markdown("---")

    st.markdown("**DEVELOPER**")
    st.markdown("**Jatin** — Full-Stack AI Engineer")
    st.markdown("[GitHub ↗](https://github.com/jatindev1022)   [LinkedIn ↗](https://www.linkedin.com/in/jatin-dev)")

    st.markdown("")
    st.markdown("**TECH STACK**")
    st.markdown("""
    `FastAPI` &nbsp; `LangGraph` &nbsp; `Llama 3.1-70B`  
    `Groq` &nbsp; `Docker` &nbsp; `Render` &nbsp; `Streamlit`
    """, unsafe_allow_html=True)

    st.markdown("")
    with st.expander("How it works"):
        st.markdown("""
        1. Your query hits the **FastAPI** backend.
        2. **LangGraph** coordinates tool calls.
        3. Agent fetches real-time weather, places, and costs.
        4. Returns a structured Markdown itinerary.
        """)


# ─────────────────────────────────────────────
# MAIN CONTENT
# ─────────────────────────────────────────────

# Badge
st.markdown("""
<div style="display:inline-block; background:#eff6ff; color:#2563eb; border:1px solid #bfdbfe;
border-radius:100px; padding:4px 14px; font-size:0.75rem; font-weight:500; margin-bottom:16px;">
🤖 Powered by LangGraph + Groq
</div>
""", unsafe_allow_html=True)

# Hero
st.markdown("""
<h1 style="font-size:2.25rem; font-weight:700; color:#111827; letter-spacing:-0.04em; line-height:1.2; margin:0 0 10px 0;">
Plan your next trip<br>with AI.
</h1>
<p style="font-size:1rem; color:#6b7280; margin:0 0 24px 0; line-height:1.6;">
Describe where you want to go. The agent will research weather,<br>
places, and costs — then build a complete itinerary for you.
</p>
""", unsafe_allow_html=True)

# Quick Suggestions
st.markdown('<p style="font-size:0.72rem; font-weight:600; color:#9ca3af; letter-spacing:0.08em; text-transform:uppercase; margin-bottom:8px;">Quick Suggestions</p>', unsafe_allow_html=True)

chip_col1, chip_col2, chip_col3, _ = st.columns([1, 1, 1, 4])
with chip_col1:
    st.markdown('<div class="chip-wrp">', unsafe_allow_html=True)
    if st.button("🗼 Paris"):
        st.session_state["q"] = "Plan a 3-day romantic trip to Paris, France."
    st.markdown('</div>', unsafe_allow_html=True)
with chip_col2:
    st.markdown('<div class="chip-wrp">', unsafe_allow_html=True)
    if st.button("🌴 Bali"):
        st.session_state["q"] = "Plan a relaxing 7-day trip to Bali, Indonesia."
    st.markdown('</div>', unsafe_allow_html=True)
with chip_col3:
    st.markdown('<div class="chip-wrp">', unsafe_allow_html=True)
    if st.button("🍜 Tokyo"):
        st.session_state["q"] = "Plan a 5-day cultural food trip in Tokyo, Japan."
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("")

# Input Form
with st.form(key="trip_form"):
    user_input = st.text_input(
        label="destination",
        value=st.session_state.get("q", ""),
        placeholder="e.g., A 5-day budget-friendly trip to Manali for two people..."
    )
    _, btn_col = st.columns([3, 1])
    with btn_col:
        submitted = st.form_submit_button("Generate Itinerary →")

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
            st.markdown('<p class="caption-text">✓ Generated by AI · Verify details before booking.</p>', unsafe_allow_html=True)
        else:
            err = res.json().get("error", res.text)
            st.error(f"Backend error: {err}")

    except Exception as e:
        st.error(f"Could not reach backend at `{BASE_URL}`.")
        st.info("On the free Render tier, the server sleeps after inactivity. Please wait 30–45 seconds and try again.")