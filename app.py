import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from datetime import datetime

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

# --- SIDEBAR ---
st.sidebar.title("📚 Techpaddi Menu")
if st.sidebar.button("🆕 Start New Chat"):
    st.session_state.messages = []
    st.session_state.chat = model.start_chat(history=[])
    st.experimental_rerun()

# Show chat history by timestamp (optional simple list)
if "history" not in st.session_state:
    st.session_state.history = []

if st.session_state.messages:
    st.sidebar.markdown("### 🕘 Chat History")
    for i, chat in enumerate(st.session_state.history[-5:][::-1]):
        st.sidebar.markdown(f"- {chat}")

# --- MAIN SECTION ---
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

# --- CHAT HISTORY DISPLAY ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        bubble_class = "user-bubble" if message["role"] == "user" else "assistant-bubble"
        st.markdown(f'<div class="{bubble_class}">{message["content"]}</div>', unsafe_allow_html=True)

# --- CHAT INPUT ---
if user_input := st.chat_input("Ask Techpaddi anything — tech, tools, tips, or career help..."):
    # Save message
    timestamp = datetime.now().strftime("%b %d, %H:%M")
    st.session_state.history.append(f"Chat on {timestamp}")
    
    # User message
    with st.chat_message("user"):
        st.markdown(f'<div class="user-bubble">{user_input}</div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Assistant response
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

# --- STYLING ---
st.markdown("""
    <style>
        .user-bubble {
            background-color: #d1e7dd;
            color: black;
            padding: 10px 15px;
            border-radius: 15px;
            margin-bottom: 8px;
            max-width: 80%;
        }
        .assistant-bubble {
            background-color: #f8d7da;
            color: black;
            padding: 10px 15px;
            border-radius: 15px;
            margin-bottom: 8px;
            max-width: 80%;
        }
    </style>
""", unsafe_allow_html=True)


