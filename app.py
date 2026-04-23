import streamlit as st
import google.generativeai as genai

# १. API Key मिळवा
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Secrets मध्ये GEMINI_API_KEY सापडली नाही!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.set_page_config(page_title="Mahi AI", page_icon="👩‍🦰")
st.title("माही: तुमची मैत्रीण 👩‍🦰")

# २. मॉडेलची निवड (हे नाव अगदी लेटेस्ट आहे)
# 'models/' हा शब्द जोडल्याने 404/NotFound एरर येत नाही
model_name = 'models/gemini-1.5-flash'

try:
    model = genai.GenerativeModel(model_name)
except Exception as e:
    st.error(f"मॉडेल लोड करताना चूक झाली: {e}")
    st.stop()

# ३. चॅट हिस्ट्री
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ४. मेसेज पाठवणे
if prompt := st.chat_input("माहीशी बोला..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # माहीला तिची ओळख करून द्या
        instruction = "Tuze nav Mahi aahe. Tu ek maitrin aahes. Marathi madhe bol. "
        response = model.generate_content(instruction + prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"काहीतरी गडबड झाली: {e}")



