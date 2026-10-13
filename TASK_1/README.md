# RuleBot AI

## About the Project

RuleBot AI is a simple chatbot developed using Python and Streamlit. It can answer common questions using predefined rules and uses Google Gemini AI to respond to questions that are not covered by those rules.

The main purpose of this project is to understand the basic working of chatbots and learn how to integrate AI into a web application. The interface is designed to be simple and easy to use.

## Features

- Responds to greetings like hello, hi, and hey.
- Answers basic questions about Python, AI, and machine learning.
- Provides jokes and motivational messages.
- Shows the current date and time.
- Uses Google Gemini AI to answer general questions.
- Displays chat history during the current session.
- Includes a clear chat option to start a fresh conversation.
- Provides a simple and interactive interface using Streamlit.

## Technologies Used

- **Python:** Used to develop the chatbot logic.
- **Streamlit:** Used to create the web interface.
- **Google Gemini AI:** Used to generate responses to general questions.
- **Regular Expressions:** Used to identify keywords and match user messages with predefined rules.

## How It Works

When a user enters a message, RuleBot AI first checks whether it matches any predefined rule. If a matching rule is found, the chatbot returns a predefined response.

If no rule matches the message, the application sends the conversation context to Google Gemini AI and displays the generated response.

This combination makes the chatbot useful for basic queries while also allowing it to handle a wider range of questions.

## Installation and Setup

Follow these steps to run the project on your local computer.

**1. Clone the repository**

```bash
git clone https://github.com/YOUR-USERNAME/RuleBot-AI.git
```

**2. Open the project folder**

```bash
cd RuleBot-AI
```

**3. Install the required libraries**

```bash
pip install -r requirements.txt
```

**4. Configure the Gemini API key**

Add your `GEMINI_API_KEY` to Streamlit Secrets or set it as an environment variable.

**5. Run the application**

```bash
streamlit run app.py
```

The application will open in your web browser.

## Learning Outcomes

While developing this project, I learned how to build a chatbot using Python, work with regular expressions, manage chat history using Streamlit session state, and integrate Google Gemini AI into an application.

This project also helped me understand the difference between rule-based responses and AI-generated responses.

## Future Improvements

In the future, I would like to add voice interaction, improve conversation memory, and include more predefined responses to make the chatbot more useful.

## Author

**Mukul Bandewar**

AI and Machine Learning Student
