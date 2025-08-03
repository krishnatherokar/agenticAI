import streamlit as st
from google import generativeai as genai

genai.configure(api_key=st.secrets["GEMINI_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Your AI Assistant")

# display chat history
for chat in st.session_state.messages:
    if chat["role"] == "user":
        st.chat_message("user").markdown(chat["content"])
    else:
        st.chat_message("assistant").markdown(chat["content"])

if prompt := st.chat_input("Type your message...", max_chars=100):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    response = model.generate_content(prompt)
    reply = response.text.strip()
    
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").markdown(reply)