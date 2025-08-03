import streamlit as st
from google import generativeai as genai
import itertools
import time

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

# scroll element
scroll_anchor = st.empty()

if prompt := st.chat_input("Type your message...", max_chars=100):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    prompt = "Instructions: You are an AI assistant created by Krishna Therokar using Gemini API and Streamlit. Provide your response to the last user message. Directly start your response without 'Gemini'.\nChat history:\n"

    # add chat history
    for msg in st.session_state.messages[-6:]:
        role = "You" if msg["role"] == "user" else "Gemini"
        prompt += f"{role}: {msg["content"]}\n"
    
    # display typing animation
    time.sleep(0.6)
    assistant_placeholder = st.chat_message("assistant")
    with assistant_placeholder:
        typing_placeholder = st.empty()
        dots = itertools.cycle(['.', '..', '...'])
        for _ in range(10):
            typing_placeholder.markdown(f"Gemini is typing{next(dots)}")
            time.sleep(0.2)
        
        try:
            response = model.generate_content(prompt)
            reply = response.text.strip()

            typing_placeholder.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})

        except Exception as e:
            error_message = "Gemini failed to respond. Please try again later."
            typing_placeholder.markdown(error_message)
            st.error(e)

    # scroll to bottom
    scroll_anchor.markdown("<div id='scroll-to-bottom'></div>", unsafe_allow_html=True)
    st.markdown("<script>const el = document.getElementById('scroll-to-bottom'); if (el) el.scrollIntoView({behavior: 'smooth'});</script>", unsafe_allow_html=True)