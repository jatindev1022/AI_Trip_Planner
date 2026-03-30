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

# --- CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"], [data-testid="stAppViewContainer"] {
    font-family: 'Inter', sans-serif !important;
}
.main .block-container {
    padding-top: 2.5rem;
    max-width: 720px;
}

/* ---- sidebar ---- */
[data-testid="stSidebar"] {
    background-color: #FAFAFA !important;
    border-right: 1px solid #EBEBEB !important;
    padding-top: 1.5rem;
}
[data-testid="stSidebar"] * {
    color: #374151 !important;
    text-decoration: none !important;
}
[data-testid="stSidebar"] a {
    color: #6B7280 !important;
    font-weight: 500;
}
[data-testid="stSidebar"] a:hover {
    color: #111827 !important;
}

/* ---- all buttons ---- */
div.stButton > button,
div.stFormSubmitButton > button {
    background-color: #FFFFFF !important;
    color: #374151 !important;
    border: 1px solid #D1D5DB !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    padding: 0.45rem 1rem !important;
    transition: all 0.15s ease !important;
}
div.stButton > button:hover,
div.stFormSubmitButton > button:hover {
    background-color: #F9FAFB !important;
    border-color: #9CA3AF !important;
    color: #111827 !important;
}

/* ---- text input ---- */
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
    box-shadow: 0 0 0 3px rgba(0,0,0,0.04) !important;
    outline: none !important;
}
.stTextInput > div > div > input::placeholder {
    color: #9CA3AF !important;
}
label[data-testid="stWidgetLabel"] { display: none !important; }

/* ---- result card ---- */
.result-card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 12px;
    padding: 28px 32px;
    line-height: 1.8;
    color: #374151;
    font-size: 0.9rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    margin-top: 16px;
}
.result-card h1, .result-card h2, .result-card h3 {
    color: #111827 !important;
    font-weight: 600;
    margin-top: 1.4em;
    border-bottom: 1px solid #F3F4F6;
    padding-bottom: 4px;
}
.result-card ul { padding-left: 1.4em; }
.result-card li { margin-bottom: 4px; }

/* ---- spinner ---- */
[data-testid="stSpinner"] > div { color: #6B7280 !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SIDEBAR  (plain text + st.markdown no links in list)
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("#### ✈️ AI Trip Planner")
    st.caption("Agentic Itinerary System · v2.0")
    st.divider()

    st.markdown("**Developer**")
    st.write("Jatin — Full-Stack AI Engineer")

    # Links as HTML so they stay plain
    st.markdown("""
    <a href="https://github.com/jatindev1022" target="_blank">GitHub</a>
    &nbsp;·&nbsp;
    <a href="https://www.linkedin.com/in/jatin-dev" target="_blank">LinkedIn</a>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("**Tech Stack**")
    # Plain text – NOT markdown links to avoid colored hyperlinks
    st.markdown("""
    <ul style="padding-left:16px; margin:0; line-height:2;">
      <li>FastAPI (Backend API)</li>
      <li>LangGraph (Agentic Logic)</li>
      <li>Llama 3.3-70B via Groq</li>
      <li>Docker + Render (Infra)</li>
      <li>Streamlit Cloud (Frontend)</li>
    </ul>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("**How it works**")
    st.markdown("""
    <ol style="padding-left:16px; margin:0; line-height:2; color:#6B7280;">
      <li>Query sent to FastAPI backend.</li>
      <li>LangGraph orchestrates tool calls.</li>
      <li>Agent fetches weather, places & costs.</li>
      <li>Returns a full itinerary in Markdown.</li>
    </ol>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MAIN CONTENT
# ─────────────────────────────────────────────
st.markdown("""
<h1 style="font-size:2rem; font-weight:700; color:#111827;
           letter-spacing:-0.03em; line-height:1.2; margin-bottom:8px;">
Plan your next trip with AI.
</h1>
<p style="font-size:0.95rem; color:#6B7280; margin-bottom:28px; line-height:1.65;">
Describe your destination. The agent researches weather, attractions,<br>
and costs — then builds a complete itinerary for you.
</p>
""", unsafe_allow_html=True)

# Quick Suggestions label
st.markdown('<p style="font-size:0.7rem; font-weight:600; color:#9CA3AF; letter-spacing:0.1em; margin-bottom:4px;">QUICK SUGGESTIONS</p>', unsafe_allow_html=True)

# Suggestion chips
c1, c2, c3, _ = st.columns([0.9, 0.9, 0.9, 5])
with c1:
    if st.button("Paris"):
        st.session_state["q"] = "Plan a 3-day romantic trip to Paris, France."
with c2:
    if st.button("Bali"):
        st.session_state["q"] = "A relaxing 7-day trip in Bali, Indonesia."
with c3:
    if st.button("Tokyo"):
        st.session_state["q"] = "A 5-day cultural food trip in Tokyo, Japan."

st.markdown("<br>", unsafe_allow_html=True)

# ---- Search Form ----
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
        with st.spinner("Researching your destination, please wait..."):
            res = requests.post(
                f"{BASE_URL}/query",
                json={"question": user_input},
                timeout=180
            )

        if res.status_code == 200:
            answer = res.json().get("answer", "No itinerary returned.")
            st.markdown(f'<div class="result-card">{answer}</div>', unsafe_allow_html=True)
            st.caption("✓ AI-generated plan. Please verify details before booking.")
        else:
            err = res.json().get("error", res.text)
            st.error(f"Backend error: {err}")

    except requests.exceptions.Timeout:
        st.error("The request timed out. The agent is taking too long to respond.")
        st.info("This usually means the AI backend on Render's free tier is waking up. Wait 30–45 seconds and try again.")
    except Exception as e:
        st.error(f"Could not reach backend at `{BASE_URL}`.")
        st.info("On the free Render tier, the server sleeps after inactivity. Wait 30–45s and try again.")