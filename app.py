import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Load Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize the Gemini model
model = genai.GenerativeModel("gemini-pro")

# Set Streamlit page config
st.set_page_config(page_title="Techpaddi Chatbot", page_icon="🤖", layout="centered")

# App title
st.title("🤖 Techpaddi - Your AI Career Buddy")

st.markdown("""
Welcome to **Techpaddi**, your friendly AI chatbot for exploring tech career paths, learning resources, and industry tips.  
Ask me anything about tech, and I will try my best to guide you!
""")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask Techpaddi something about tech careers..."):
    # Show user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Show typing spinner
    with st.chat_message("assistant"):
        with st.spinner("Techpaddi is thinking..."):
            try:
                response = model.generate_content(prompt)
                reply = response.text
            except Exception as e:
                reply = "⚠️ Sorry, I encountered an error. Please try again."
                print(e)

            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
