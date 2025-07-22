import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize Gemini model
model = genai.GenerativeModel("gemini-pro")

# Page settings
st.set_page_config(
    page_title="Techpaddi Chatbot",
    page_icon="🤖",
    layout="centered"
)

# App title and intro
st.title("🤖 Techpaddi - Your AI Career Buddy")
st.markdown("Welcome to **Techpaddi**, your AI guide to all things tech, careers, and digital growth.")

# About section (collapsible)
with st.expander("💬 About Techpaddi"):
    st.markdown("""
    **Techpaddi** is your AI-powered assistant designed to help with **anything tech-related** — and more.

    Ask me things like:
    - *"How do I switch to tech from a non-tech background?"*
    - *"What are the latest tools in AI?"*
    - *"Write a social media strategy for a tech product"*
    - *"What’s the best beginner laptop for design?"*
    - *"Explain blockchain to a 5-year-old"*

    I’m always here to help. Just type your question below 👇
    """)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask Techpaddi anything — tech, tools, tips, or career help..."):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Gemini AI response
    with st.chat_message("assistant"):
        with st.spinner("Techpaddi is thinking..."):
            try:
                response = model.generate_content(
                    f"You are Techpaddi, an AI assistant that answers open-ended questions in a helpful and friendly tone.\n\nUser: {prompt}\nTechpaddi:"
                )
                reply = response.text
            except Exception as e:
                reply = "⚠️ Sorry, I encountered an error. Please try again."
                print("Error:", e)

            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})

