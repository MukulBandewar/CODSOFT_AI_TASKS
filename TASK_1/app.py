import random
import re
import os
from datetime import datetime

import streamlit as st
import google.generativeai as genai

st.set_page_config(
    page_title="RuleBot AI",
    page_icon="🤖",
    layout="centered"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    color: #f8fafc;
    font-family: 'Segoe UI', Roboto, sans-serif;
}
.main-title {
    text-align: center;
    font-size: 3.2rem !important;
    font-weight: 800;
    background: linear-gradient(45deg, #3b82f6, #8b5cf6, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0;
}
.main-caption {
    text-align: center;
    color: #94a3b8;
    font-size: 1.1rem;
    margin-bottom: 2rem;
}
.stButton>button {
    width: 100%;
    border-radius: 12px;
    background: linear-gradient(90deg, #ef4444 0%, #dc2626 100%) !important;
    color: white !important;
    border: none !important;
    font-weight: 600 !important;
    padding: 0.6rem 1rem !important;
    transition: all 0.3s ease;
}
.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(239, 68, 68, 0.4);
}
hr {
    border-color: #334155 !important;
    margin: 2rem 0 !important;
}
.developer-credit {
    position: fixed;
    bottom: 12px;
    right: 18px;
    color: #cbd5e1;
    font-size: 12px;
    z-index: 999;
    background: rgba(15, 23, 42, 0.95);
    padding: 6px 10px;
    border-radius: 8px;
    border: 1px solid #334155;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<h1 class="main-title">🤖 RuleBot AI</h1>',
    unsafe_allow_html=True
)
st.markdown(
    '<p class="main-caption">Rule-based chatbot + Gemini AI Intelligence</p>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="developer-credit">Developer: Mukul Bandewar</div>
""", unsafe_allow_html=True)


def get_api_key():
    try:
        key = st.secrets.get("GEMINI_API_KEY")
        if key:
            return str(key).strip()
    except Exception:
        pass
    return os.getenv("GEMINI_API_KEY", "").strip()


responses = {
    r"\b(hi|hello|hey)\b": [
        "Hello! How can I help you?",

