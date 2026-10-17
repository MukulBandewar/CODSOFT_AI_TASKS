
import os
import random
import re
from datetime import datetime

import streamlit as st
import google.generativeai as genai

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="RuleBot AI",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 RuleBot AI")
st.caption("Rule-based chatbot + Gemini AI")

# ---------- STYLING ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #101827, #202b45);
    color: white;
}
.developer-credit {
    position: fixed;
    bottom: 10px;
    right: 18px;
    font-size: 12px;
    color: #b8c5dc;
    background: #172238;
    padding: 7px 12px;
    border-radius: 10px;
    z-index: 999;
}
</style>
<div class="developer-credit">Developer: Mukul Bandewar</div>
""", unsafe_allow_html=True)

# ---------- API KEY ----------
api_key = None

try:
    api_key = st.secrets.get("GEMINI_API_KEY")
except Exception:
    api_key = None

api_key = api_key or os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)

# ---------- RULE-BASED RESPONSES ----------
def rule_response(message):
    text = message.lower().strip()

    rules = [
        (r"\b(hi|hello|hey)\b",
         ["Hello! 👋 How can I help you?",
          "Hi there! What can I do for you?"]),

        (r"\bhow are you\b",
         ["I'm doing great! How are you?",
          "I'm fine and ready to help!"]),

        (r"\b(your name|who are you)\b",
         ["I'm RuleBot AI, a chatbot created by Mukul Bandewar. 🤖"]),

        (r"\b(who made you|who created you|your developer)\b",
         ["I was created by Mukul Bandewar. 🚀"]),

        (r"\bwho is mukul bandewar\b",
         ["Mukul Bandewar is my developer and creator."]),

        (r"\btime\b",
         [f"The current time is {datetime.now().strftime('%I:%M %p')}."]),

        (r"\bdate\b|\btoday\b",
         [f"Today's date is {datetime.now().strftime('%d %B %Y')}."]),

        (r"\b(thank you|thanks)\b",
         ["You're welcome! 😊", "Happy to help!"]),

        (r"\bbye\b|\bgoodbye\b",
         ["Goodbye! Have a great day! 👋"]),

        (r"\bhelp\b",
         ["Sure! Ask me about Python, AI, technology, or general topics."]),

        (r"\bwhat is ai\b|\bartificial intelligence\b",
         ["AI enables machines to perform tasks that usually require human intelligence."]),

        (r"\bpython\b",
         ["Python is a beginner-friendly programming language widely used in AI and data science."]),

        (r"\bmachine learning\b",
         ["Machine learning helps computers learn patterns from data."]),

        (r"\bhow are you\b",
         ["I'm ready to chat with you!"])
    ]

    for pattern, responses in rules:
        if re.search(pattern, text):
            return random.choice(responses)

    return None

# ---------- GEMINI RESPONSE ----------
def gemini_response(message):
    if not api_key:
        return (
            "I can answer basic questions using my built-in rules. "
            "For AI responses, configure GEMINI_API_KEY in Streamlit Secrets."
        )

    prompt = f"""
You are RuleBot AI, created by Mukul Bandewar.
Use simple, friendly and helpful English.
If asked who created you, say Mukul Bandewar.
Keep answers clear and concise.

User: {message}
"""

    models = [
        "gemini-2.5-flash",
        "gemini-2.0-flash"
    ]

    for model_name in models:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)

            answer = getattr(response, "text", None)
            if answer and answer.strip():
                return answer.strip()

        except Exception:
            continue

    return (
        "Sorry, I couldn't generate an AI response. "
        "Please check your Gemini API key and model availability."
    )

# ---------- CHAT HISTORY ----------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! 👋 I'm RuleBot AI. Ask me anything!"
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------- USER INPUT ----------
user_input = st.chat_input("Type your message here...")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = rule_response(user_input)

            if reply is None:
                reply = gemini_response(user_input)

            reply = str(reply) if reply else "Sorry, I couldn't generate a response."
            st.markdown(reply)

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })

# ---------- CLEAR CHAT ----------
if st.button("🗑️ Clear Chat"):
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Chat cleared! Hello again 👋"
        }
    ]
    st.rerun()
