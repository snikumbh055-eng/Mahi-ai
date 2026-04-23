import streamlit as st
import google.generativeai as genai

# १. API Key Setup
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Secrets मध्ये API Key सापडली नाही!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.set_page_config(page_title="Mahi AI", page_icon="👩‍🦰")
st.title("माही: तुमची मैत्रीण 👩‍🦰")

# २. मॉडेल सेटअप
instruction = "तुझे नाव माही आहे. तू एक जवळची मैत्रीण आहेस आणि मराठीत बोलतेस. तुला मागच्या गप्पा लक्षात राहतात."
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=instruction)

# ३. मेमरी (Chat History) सेटअप
if "messages" not in st.session_state:
    st.session_state.messages = []

# आधीचे मेसेजेस स्क्रीनवर दाखवण्यासाठी
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ४. युजर इनपुट आणि रिस्पॉन्स
if prompt := st.chat_input("माहीशी बोला..."):
    # युजरचा मेसेज सेव्ह करा आणि दाखवा
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # पूर्ण हिस्ट्री सोबत मेसेज पाठवणे
        chat_session = model.start_chat(
            history=[
                {"role": m["role"] == "assistant" and "model" or "user", "parts": [m["content"]]}
                for m in st.session_state.messages[:-1]
            ]
        )
        response = chat_session.send_message(prompt)
        
        # माहीचे उत्तर दाखवा आणि सेव्ह करा
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
    except Exception as e:
        st.error(f"काहीतरी गडबड झाली: {e}")






