
import random
import re
import os
from datetime import datetime

import streamlit as st
from google import genai


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="RuleBot AI",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 RuleBot AI")
st.caption("Rule-based chatbot + Gemini AI")


# ---------------- API KEY ----------------
def get_api_key():
    # First try Streamlit Secrets
    try:
        key = st.secrets.get("GEMINI_API_KEY")
        if key:
            return str(key).strip()
    except Exception:
        pass

    # Then try environment variable
    return os.getenv("GEMINI_API_KEY", "").strip()


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
        "I was built using Python, Streamlit, and Google Gemini AI."
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
            "I can answer basic questions, tell jokes, show the date "
            "and time, and answer other questions using Gemini AI."
        )

    for pattern, replies in responses.items():
        if re.search(pattern, user):
            return random.choice(replies)

    return None


# ---------------- GEMINI AI ----------------
def get_ai_response():
    api_key = get_api_key()

    if not api_key:
        return (
            "⚠️ Gemini API key is missing. Add GEMINI_API_KEY "
            "to Streamlit Secrets or your environment variables."
        )

    try:
        client = genai.Client(api_key=api_key)

        # Include recent chat messages for context
        history = st.session_state.messages[-12:]

        conversation_text = "\n".join(
            f"{'User' if msg['role'] == 'user' else 'RuleBot'}: "
            f"{msg['content']}"
            for msg in history
        )

        prompt = (
            "You are RuleBot AI, a friendly and helpful assistant. "
            "Answer the user's latest message accurately in simple language. "
            "Use examples when useful. If you are unsure, say so.\n\n"
            "Conversation history:\n"
            f"{conversation_text}\n\n"
            "Answer the latest user message."
        )

        # Try the primary model, then a fallback model
        models = ["gemini-3.8-flash", "gemini-3.6-flash"]
        last_error = None

        for model_name in models:
            try:
                result = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )

                answer = getattr(result, "text", None)

                if answer and answer.strip():
                    return answer.strip()

                last_error = f"{model_name} returned an empty response."

            except Exception as error:
                last_error = f"{model_name}: {error}"

        # Show the actual error so you can diagnose it
        st.error(f"Gemini API error: {last_error}")

        return (
            "Sorry, Gemini could not answer. Please check the error "
            "shown above, your API key, model access, and API quota."
        )

    except Exception as error:
        st.error(f"Gemini setup error: {error}")
        return "Sorry, the AI service could not be started."


# ---------------- CHAT HISTORY ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ---------------- CHAT INPUT ----------------
if prompt := st.chat_input("Ask me anything..."):
    prompt = prompt.strip()

    if not prompt:
        st.warning("Please enter a message.")
        st.stop()

    # Save and display user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # Try rules first, Gemini second
    with st.chat_message("assistant"):
        with st.spinner("RuleBot is thinking..."):
            reply = get_rule_response(prompt.lower())

            if reply is None:
                reply = get_ai_response()

            st.markdown(reply)

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })


# ---------------- CLEAR CHAT ----------------
if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()

