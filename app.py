

import random
import re
import os
from datetime import datetime

import streamlit as st
from openai import OpenAI


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="RuleBot AI",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 RuleBot AI")
st.caption("Rule-based chatbot + AI-powered answers")


# ---------------- API CONFIGURATION ----------------
def get_api_key():
    try:
        return st.secrets["OPENAI_API_KEY"]
    except (KeyError, FileNotFoundError):
        return os.getenv("OPENAI_API_KEY")


# ---------------- RULE-BASED RESPONSES ----------------
responses = {
    r"\b(hi|hello|hey)\b": [
        "Hello! How can I help you?",
        "Hi there! Welcome to RuleBot.",
        "Hey! Nice to meet you."
    ],
    r"\bhow are you\b": [
        "I'm doing great! How are you?",
        "I'm fine, thanks for asking!"
    ],
    r"\b(your name|who are you)\b": [
        "I'm RuleBot AI, your Python chatbot."
    ],
    r"\b(your age|how old are you)\b": [
        "I'm an AI chatbot, so I don't have a human age."
    ],
    r"\b(who made you|who created you|creator)\b": [
        "I was built using Python, Streamlit, and an AI API."
    ],
    r"\b(what is python|define python)\b": [
        "Python is a popular programming language known for its readable syntax."
    ],
    r"\b(what is ai|artificial intelligence)\b": [
        "Artificial intelligence enables computers to perform tasks that typically require human intelligence."
    ],
    r"\b(machine learning|what is ml)\b": [
        "Machine learning helps computers learn patterns from data."
    ],
    r"\b(joke|tell me a joke)\b": [
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "Why was the computer cold? It left its Windows open!"
    ],
    r"\b(thanks|thank you)\b": [
        "You're welcome! Happy to help."
    ],
    r"\b(bye|goodbye|exit|quit)\b": [
        "Goodbye! Have a wonderful day."
    ]
}


def get_rule_response(user):
    # Dynamic date and time
    if re.search(r"\b(time|clock)\b", user):
        return "Current time: " + datetime.now().strftime("%I:%M %p")

    if re.search(r"\b(date|today)\b", user):
        return "Today's date: " + datetime.now().strftime("%d-%m-%Y")

    if re.search(r"\b(motivate me|motivation)\b", user):
        return random.choice([
            "Believe in yourself. Every expert was once a beginner!",
            "Keep learning and never give up on your dreams!"
        ])

    if re.search(r"\b(help|what can you do)\b", user):
        return (
            "I can answer basic questions, tell jokes, "
            "show the date and time, and answer other questions using AI."
        )

    for pattern, replies in responses.items():
        if re.search(pattern, user):
            return random.choice(replies)

    # None means this question needs an AI response
    return None


# ---------------- AI RESPONSE ----------------
def get_ai_response(user):
    api_key = get_api_key()

    if not api_key:
        return (
            "AI API key is missing. Add OPENAI_API_KEY "
            "in Streamlit Secrets or your environment variables."
        )

    try:
        client = OpenAI(api_key=api_key)

        # Keep recent conversation context
        history = st.session_state.messages[-12:]

        conversation = [
            {
                "role": "system",
                "content": (
                    "You are RuleBot AI, a friendly and helpful assistant. "
                    "Answer the user's question clearly and accurately. "
                    "Use simple language and give examples when useful. "
                    "If you are unsure, say so rather than inventing facts."
                )
            }
        ]

        for message in history:
            conversation.append({
                "role": message["role"],
                "content": message["content"]
            })

        result = client.responses.create(
            model="gpt-6-astra",
            input=conversation,
            max_output_tokens=500
        )

        return result.output_text

    except Exception as error:
        st.error("AI service could not respond. Check your API key, "
                 "API access, account quota, and connection.")
        return "Sorry, I couldn't generate an answer right now."


# ---------------- CHAT HISTORY ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ---------------- CHAT INPUT ----------------
if prompt := st.chat_input("Ask me anything..."):
    user = prompt.strip().lower()

    if not user:
        st.warning("Please enter a message.")
        st.stop()

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("RuleBot is thinking..."):

            # Check rules first
            reply = get_rule_response(user)

            # Unknown question goes to the AI API
            if reply is None:
                reply = get_ai_response(user)

            st.markdown(reply)

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })


# ---------------- CLEAR CHAT ----------------
if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()
