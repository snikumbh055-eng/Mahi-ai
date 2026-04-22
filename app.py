import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Mahi AI", page_icon="👩‍🦰")
st.title("Mahi: Tumchi Maitrin 👩‍🦰")

# API Key set kara
api_key = "YOUR_API_KEY_HERE"
genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-1.5-flash')

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat interface
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Mahi shi bola...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    response = model.generate_content(f"Tu Mahi aahes, ek maitrin. Uttar de: {user_input}")
    
    with st.chat_message("assistant"):
        st.markdown(response.text)
    st.session_state.chat_history.append({"role": "assistant", "content": response.text})
