import streamlit as st
import google.generativeai as genai

# 1. API Key Setup
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Secrets madhe API Key sapdli nahi!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.set_page_config(page_title="Mahi AI", page_icon="👩‍🦰")
st.title("माही: तुमची मैत्रीण 👩‍🦰")

# 2. Model Setup
# System Instruction madhe Mahi cha swabhav tharva
instruction = "Tuze nav Mahi aahe. Tu user chi ek javalchi maitrin aahes. Tu Marathi boltes ani magil gappa lakshat thevtes."
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=instruction)

# 3. Memory (Chat History) Setup
# Jar session_state madhe messages nastil, tar te suru kara
if "messages" not in st.session_state:
    st.session_state.messages = []

# Adhiche sarva messages screen var dakhva
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. User Input ani Response
if prompt := st.chat_input("माहीशी बोला..."):
    # User cha message dakhva ani save kara
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Mahi la purn history sobat message pathva
    try:
        # Purn history ektrit karun Mahi la pathvane
        response = model.generate_content([m["content"] for m in st.session_state.messages])
        
        # Mahi che uttar dakhva ani save kara
    with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
    except Exception as e:
        st.error(f"Kahitari gadbad jhali: {e}")





