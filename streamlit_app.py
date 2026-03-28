import streamlit as st
import datetime
import requests
import sys


BASE_URL='http://localhost:8000'#end point baceknd

st.set_page_config(
    page_title=" Travel Planner Agentic application",
    page_icon="# ",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title(" Travel Planner Agentic application")

if "messages" not in st.session_state:
    st.session_state.message=[]
    
st.header("Hii how can i help you planninf a trip? let me know where you you want to visit?")

with st.form():
    user_input=""
    submit_button=""

if submit_button and user_input.strip():
    try:
        with st.spinner("bot is thinking.."):
            payload={"question":user_input}
            response=requests.post(f"{BASE_URL}/query",json=payload)
            
        if response.status_code==200:
            answer=response.json().get("answer","No answer return try again.")
            markdown_content=f"""
            # Ai travel agent
            ---
            {answer}
            ---
            "this travel plan was genrated by ai please verify all the information,prices etc"
            
            
            
            """
    except Exception as e:
        raise f"The response failed due to {e}"
    