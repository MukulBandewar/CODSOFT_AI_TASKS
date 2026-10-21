
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

.stButton > button {
    width: 100%;
    border-radius: 12px;
    background: linear-gradient(90deg, #ef4444, #dc2626) !important;
    color: white !important;
    border: none !important;
    font-weight: 600 !important;
    padding: 0.6rem 1rem !important;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(239, 68, 68, 0.4);
}

hr {
    border-color: #334155 !important;
    margin: 2rem 0 !important;
}

.developer-credit {
    position: fixed;
    bottom: 10px;
    right: 12px;
    color: #cbd5e1;
    font-size: 12px;
    z-index: 999;
    background: rgba(15, 23, 42, 0.95);
    padding: 6px 10px;
    border-radius: 8px;
    border: 1px solid #334155;
    pointer-events: none;
}

/* Tablet and mobile responsive design */
@media screen and (max-width: 768px) {
    .main-title {
        font-size: 2.2rem !important;
        line-height: 1.2;
    }

    .main-caption {
        font-size: 0.95rem;
        margin-bottom: 1.2rem;
        padding: 0 8px;
    }

    .block-container {
        padding: 1rem 1rem 5rem 1rem !important;
    }

    .stButton > button {
        min-height: 44px;
        font-size: 0.95rem !important;
        transform: none;
    }

    .developer-credit {
        bottom: 6px;
        right: 6px;
        font-size: 10px;
        padding: 4px 7px;
    }

    [data-testid="stChatInput"] {
        padding-bottom: 0.5rem;
    }

    [data-testid="stChatMessage"] {
        padding: 0.75rem 0.5rem;
    }

    hr {
        margin: 1.2rem 0 !important;
    }
}

/* Small mobile screens */
@media screen and (max-width: 380px) {
    .main-title {
        font-size: 1.8rem !important;
    }

    .main-caption {
        font-size: 0.85rem;
    }

    .block-container {
        padding-left: 0.7rem !important;
        padding-right: 0.7rem !important;
    }

    .developer-credit {
        font-size: 9px;
    }
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
<div class="developer-credit">
    Developer: Mukul Bandewar
</div>
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
        "Hi there! Welcome to RuleBot.",
        "Hey! Nice to meet you."
    ],
    r"\bhow are you\b": [
        "I'm doing great! How are you?",
        "I'm fine, thanks for asking!"
    ],
    r"\b(what is your name|your name|who are you)\b": [
        "I'm RuleBot AI, developed by Mukul Bandewar!"
    ],
    r"\b(who is mukul bandewar|who is mukul)\b": [
        "Mukul Bandewar is my developer. He built me using Python, Streamlit, and Google Gemini AI."
    ],
    r"\b(your age|how old are you)\b": [
        "I'm an AI chatbot, so I don't have a human age."
    ],
    r"\b(who made you|who created you|creator|developer)\b": [
        "I was created by Mukul Bandewar using Python, Streamlit, and Google Gemini AI."
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


def get_ai_response():
    api_key = get_api_key()

    if not api_key:
        return (
            "⚠️ Gemini API key is missing. Add GEMINI_API_KEY "
            "to Streamlit Secrets or your environment variables."
        )

    try:
        genai.configure(api_key=api_key)

        history = st.session_state.messages[-12:]
        conversation_text = "\n".join(
            f"{'User' if msg['role'] == 'user' else 'RuleBot'}: "
            f"{msg['content']}"
            for msg in history
        )

        full_prompt = (
            "You are RuleBot AI, developed by Mukul Bandewar. "
            "If asked who created or developed you, credit Mukul Bandewar. "
            "Answer the user's latest message accurately in simple language. "
            "Use examples when useful. If unsure, say so.\n\n"
            f"Conversation history:\n{conversation_text}\n\n"
            "Answer the latest user message."
        )

        models = [
            "gemini-2.5-flash",
            "gemini-2.5-pro",
            "gemini-3.5-flash-lite"
        ]

        last_error = None

        for model_name in models:
            try:
                model = genai.GenerativeModel(
                    model_name=model_name,
                    system_instruction=(
                        "You are RuleBot AI, a friendly and helpful assistant. "
                        "You were developed by Mukul Bandewar using Python, "
                        "Streamlit, and Google Gemini AI. "
                        "Answer accurately in simple language. "
                        "Use examples when useful. If unsure, say so."
                    )
                )

                result = model.generate_content(full_prompt)
                answer = getattr(result, "text", None)

                if answer and answer.strip():
                    return answer.strip()

                last_error = f"{model_name} returned an empty response."

            except Exception as error:
                last_error = f"{model_name}: {error}"

        st.error(f"Gemini API error: {last_error}")

        return (
            "Sorry, Gemini could not answer. Please check the error "
            "shown above, your API key, model access, and API quota."
        )

    except Exception as error:
        st.error(f"Gemini setup error: {error}")
        return "Sorry, the AI service could not be started."


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if user_prompt := st.chat_input("Ask me anything..."):
    user_prompt = user_prompt.strip()

    if not user_prompt:
        st.warning("Please enter a message.")
        st.stop()

    st.session_state.messages.append({
        "role": "user",
        "content": user_prompt
    })

    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner("✨ RuleBot is thinking..."):
            reply = get_rule_response(user_prompt.lower())

            if reply is None:
                reply = get_ai_response()

            reply = str(reply) if reply is not None else (
                "Sorry, I couldn't generate a response."
            )

            st.markdown(reply)

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })


st.markdown("---")

col1, col2, col3 = st.columns([1, 1, 1])

with col3:
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()


