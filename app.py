import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BOT_NAME = "Techpaddi"
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

# Streamlit config
st.set_page_config(
    page_title=f"{BOT_NAME} Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Title
st.markdown(f"<h1 style='text-align: center;'>🤖 {BOT_NAME} - Your AI Career Buddy</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'>Welcome to <b>{BOT_NAME}</b>, your AI guide to all things tech, careers, and digital growth.</p>", unsafe_allow_html=True)

# About Section
with st.expander("💬 About Techpaddi"):
    st.markdown(f"""
    **{BOT_NAME}** is your AI-powered assistant designed to help with:
    
    - *Tech career advice*
    - *Switching to tech*
    - *AI tools & resources*
    - *Beginner-friendly tech topics*
    
    Just ask your question below! 👇
    """)

# Initialize chat
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(f'<div class="{message["role"]}-bubble">{message["content"]}</div>', unsafe_allow_html=True)

# User input
if user_input := st.chat_input("Ask Techpaddi anything — tech, tools, tips, or career help..."):
    with st.chat_message("user"):
        st.markdown(f'<div class="user-bubble">{user_input}</div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Techpaddi is thinking..."):
            try:
                prompt = f"You are {BOT_NAME}, a helpful and friendly AI for tech career advice.\n\nUser: {user_input}\n{BOT_NAME}:"
                response = st.session_state.chat.send_message(prompt)
                reply = response.text.strip()
            except Exception as e:
                reply = "⚠️ Oops! Something went wrong. Please try again."
                st.error(f"Gemini Error: {e}")

            st.markdown(f'<div class="assistant-bubble">{reply}</div>', unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": reply})


