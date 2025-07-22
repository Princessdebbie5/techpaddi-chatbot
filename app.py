import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set bot name
BOT_NAME = "Techpaddi"

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize Gemini model
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

# Set Streamlit page config
st.set_page_config(
    page_title=f"{BOT_NAME} Chatbot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="auto"

)
    st.markdown("""
    <style>
    .user-bubble {
        background-color: #d1e7dd;
        color: #000;
        padding: 10px 15px;
        border-radius: 20px;
        margin-bottom: 8px;
        max-width: 80%;
        align-self: flex-end;
    }
    .assistant-bubble {
        background-color: #f8d7da;
        color: #000;
        padding: 10px 15px;
        border-radius: 20px;
        margin-bottom: 8px;
        max-width: 80%;
        align-self: flex-start;
    }
    </style>
""", unsafe_allow_html=True) 

# App title and header
st.title(f"🤖 {BOT_NAME} - Your AI Career Buddy")
st.markdown(f"Welcome to **{BOT_NAME}**, your AI guide to all things tech, careers, and digital growth.")

# Collapsible about section
with st.expander("💬 About Techpaddi"):
    st.markdown(f"""
    **{BOT_NAME}** is your AI-powered assistant designed to help with **anything tech-related** — and more.

    Ask me things like:
    - *"How do I switch to tech from a non-tech background?"*
    - *"What are the latest tools in AI?"*
    - *"Write a social media strategy for a tech product"*
    - *"What’s the best beginner laptop for design?"*
    - *"Explain blockchain to a 5-year-old"*

    I’m always here to help. Just type your question below 👇
    """)

# Initialize chat session
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if user_input := st.chat_input("Ask Techpaddi anything — tech, tools, tips, or career help..."):
    # Display user's message
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Generate Gemini response
    with st.chat_message("assistant"):
        with st.spinner("Techpaddi is thinking..."):
            try:
                full_prompt = f"You are {BOT_NAME}, an AI assistant that answers open-ended questions in a helpful and friendly tone.\n\nUser: {user_input}\n{BOT_NAME}:"
                response = st.session_state.chat.send_message(full_prompt)
                reply = response.text.strip()
            except Exception as e:
                reply = "⚠️ Sorry, I encountered an error. Please try again."
                st.error(f"Gemini Error: {e}")

            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})

