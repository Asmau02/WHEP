import os
import streamlit as st

def get_groq_api_key():
    """Read the Groq key from Streamlit secrets or an environment variable."""
    try:
        key = st.secrets.get("GROQ_API_KEY", "")
    except Exception:
        key = ""
    return key or os.getenv("GROQ_API_KEY", "")
