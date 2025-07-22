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
model = genai.GenerativeModel("gemini-pro")

# Set Streamlit page config
st.set_page_config(
    page_title=f"{BOT_NAME} Chatbot",
    page_icon="🤖",
    layout="centered"
)

# App title and header
st.title(f"🤖 {Techpaddi} - Your AI Career Buddy")
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

# Initialize session chat if not already created
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input box for new user message
if prompt := st.chat_input("Ask Techpaddi anything — tech, tools, tips, or career help..."):
    # Show user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate Gemini response
    with st.chat_message("assistant"):
        with st.spinner("Techpaddi is thinking..."):
            try:
                # Add context to the message
                full_prompt = f"You are {BOT_NAME}, a friendly and smart AI that helps beginners explore tech careers and learn useful resources.\n\nUser: {prompt}\n{BOT_NAME}:"
                response = st.session_state.chat.send_message(full_prompt)
                reply = response.text.strip()
            except Exception as e:
                reply = "⚠️ Sorry, I encountered an error. Please try again."
                print("Gemini Error:", e)

            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})


