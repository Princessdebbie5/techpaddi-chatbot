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

# Initialize model
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

# Streamlit config
st.set_page_config(
    page_title=f"{BOT_NAME} Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Sidebar
with st.sidebar:
    st.markdown(f"## 🤖 {BOT_NAME}")
    if st.button("New Chat"):
        st.session_state.messages = []
        st.experimental_rerun()

    st.markdown("### Chat History")
    if "messages" in st.session_state and st.session_state.messages:
        for i, msg in enumerate(st.session_state.messages):
            st.markdown(f"- {msg['role'].capitalize()}: {msg['content'][:40]}{'...' if len(msg['content']) > 40 else ''}")

    st.markdown("---")
    st.markdown("⚙️ *Future features*: Login, Themes, Export Chat")

# Page title and description
st.markdown(f"<h1 style='text-align: center;'>🤖 {BOT_NAME} - Your AI Career Buddy</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'>Welcome to <b>{BOT_NAME}</b>, your AI guide to all things tech, careers, and digital growth.</p>", unsafe_allow_html=True)

# About section
with st.expander("💬 About Techpaddi"):
    st.markdown(f"""
    **{BOT_NAME}** is your AI-powered assistant designed to help with:
    
    - *Tech career advice*
    - *Switching to tech*
    - *AI tools & resources*
    - *Beginner-friendly tech topics*

    Just ask your question below! 
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
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        with st.spinner("Techpaddi is thinking..."):
            try:
                prompt = f"You are {BOT_NAME}, a helpful and friendly AI for tech career advice.\n\nUser: {user_input}\n{BOT_NAME}:"
                response = st.session_state.chat.send_message(prompt)
                reply = response.text.strip()
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                reply = "⚠️ Oops! Something went wrong. Please try again."
                st.error(f"Gemini Error: {e}")
