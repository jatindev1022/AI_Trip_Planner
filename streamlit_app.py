import streamlit as st
import requests
import os

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="AI Voyager | Professional Travel Agent",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- BACKEND CONNECTION ---
BASE_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# --- CUSTOM THEME & CSS ---
st.markdown("""
<style>
    /* Google Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');

    /* Global Typography */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #1E293B;
    }

    /* Minimalist Sidebar */
    [data-testid="stSidebar"] {
        background-color: #F8FAFC;
        border-right: 1px solid #E2E8F0;
    }

    /* Clean Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        border: none;
        background-color: #0F172A;
        color: white;
        font-weight: 500;
        padding: 0.6rem 1rem;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #334155;
        border: none;
    }

    /* Simple Input Fields */
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 1px solid #E2E8F0;
    }

    /* Results Header Styling */
    .results-header {
        font-weight: 600;
        font-size: 1.25rem;
        margin-bottom: 1rem;
        color: #0F172A;
    }

    /* Clean Result Container */
    .result-card {
        padding: 24px;
        border-radius: 12px;
        background-color: #FFFFFF;
        border: 1px solid #F1F5F9;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        line-height: 1.7;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### **AI Voyager**")
    st.caption("v2.0 • Agentic Itinerary System")
    st.markdown("---")
    
    with st.expander("👤 **Developer Profile**", expanded=True):
        st.markdown("""
        **Jatin**  
        Full-Stack AI Developer
        
        [GitHub](https://github.com/jatindev1022) | [LinkedIn](https://www.linkedin.com/in/jatin-dev)
        """)
    
    with st.expander("🛠 **Technical Architecture**"):
        st.markdown("""
        - **Backend**: FastAPI (Python 3.12)
        - **Agentic Logic**: LangGraph 
        - **Model**: Llama 3.1-70B (Groq)
        - **Infrastructure**: Docker + Render
        """)

    st.markdown("---")
    st.caption("This system uses Agentic Reasoning to generate optimal travel paths based on real-time data.")

# --- MAIN HERO SECTION ---
st.markdown("<h1 style='color: #0F172A;'>Search Your Destination.</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #64748B; font-size: 1.1rem; margin-top: -10px;'>An autonomous travel agent powered by LangGraph.</p>", unsafe_allow_html=True)

# --- SEARCH PANEL ---
with st.container():
    # Example Selection
    example_cols = st.columns([1, 1, 1, 1.5])
    if example_cols[0].button("Paris"):
        st.session_state["query_input"] = "Plan a 3-day trip to Paris."
    if example_cols[1].button("Bali"):
        st.session_state["query_input"] = "7-day relaxation trip in Bali."
    if example_cols[2].button("Tokyo"):
        st.session_state["query_input"] = "5-day tour of Tokyo temples & food."
    
    # Input Form
    with st.form(key="travel_form", clear_on_submit=False):
        user_input = st.text_input(
            "", 
            value=st.session_state.get("query_input", ""),
            placeholder="e.g., A budget-friendly week in New York..."
        )
        col_btn_l, col_btn_r = st.columns([1, 4])
        submit_button = col_btn_l.form_submit_button(label="Generate Itinerary")

# --- RESULT SECTION ---
if submit_button and user_input.strip():
    try:
        # Subtle Loading Indicator
        with st.spinner("Analyzing destination and calculating costs..."):
            payload = {"question": user_input} 
            response = requests.post(f"{BASE_URL}/query", json=payload)
            
            if response.status_code == 200:
                answer = response.json().get("answer", "No response found.")
                
                st.markdown("---")
                st.markdown("<div class='results-header'>Travel Itinerary & Budget</div>", unsafe_allow_html=True)
                
                # Display final result in a clean "card"
                st.markdown(f"""
                <div class='result-card'>
                {answer}
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("---")
                st.success("Analysis Complete.")
            else:
                st.error("There was an issue reaching the AI backend. Please verify your Render server is active.")
                
    except Exception as e:
        st.error(f"Error: Connection to {BASE_URL} failed.")
        st.info("The backend server likely dropped to 'Sleep' mode. Please wait 45 seconds and try again.")