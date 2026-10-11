
import streamlit as st
import random
import re
from datetime import datetime

st.set_page_config(page_title="RuleBot Chatbot", page_icon="🤖")

st.title("🤖 RuleBot Chatbot")
st.caption("A simple rule-based chatbot built with Python")

responses = {
    r"\b(hi|hello|hey)\b": [
        "Hello! How can I help you?",
        "Hi there! Welcome to RuleBot."
    ],
    r"\bhow are you\b": [
        "I'm doing great! How are you?",
        "I'm fine! Thanks for asking."
    ],
    r"\b(your name|who are you)\b": [
        "My name is RuleBot, your Python chatbot."
    ],
    r"\b(what is python|define python)\b": [
        "Python is a popular programming language."
    ],
    r"\b(what is ai|artificial intelligence)\b": [
        "AI enables machines to perform tasks that usually require human intelligence."
    ],
    r"\b(machine learning|what is ml)\b": [
        "Machine learning helps computers learn patterns from data."
    ],
    r"\b(joke|tell me a joke)\b": [
        "Why do programmers prefer dark mode? Because light attracts bugs!"
    ],
    r"\b(thanks|thank you)\b": [
        "You're welcome! Happy to help."
    ],
    r"\b(bye|goodbye|exit|quit)\b": [
        "Goodbye! Have a great day."
    ]
}

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    user = prompt.strip().lower()

    if not user:
        reply = "Please enter a message."
    elif re.search(r"\b(time|clock)\b", user):
        reply = "Current time: " + datetime.now().strftime("%I:%M %p")
    elif re.search(r"\b(date|today)\b", user):
        reply = "Today's date: " + datetime.now().strftime("%d-%m-%Y")
    else:
        reply = "Sorry, I don't understand. Try asking about Python, AI, or jokes."

        for pattern, answers in responses.items():
            if re.search(pattern, user):
                reply = random.choice(answers)
                break

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )
    st.rerun()

if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

