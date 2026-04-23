import streamlit as st
import google.generativeai as genai

# १. Secrets मधून सुरक्षितपणे API Key मिळवा
if "GEMINI_API_KEY" not in st.secrets:
    st.error("कृपया Streamlit Settings मध्ये 'GEMINI_API_KEY' सेट करा!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.set_page_config(page_title="Mahi AI", page_icon="👩‍🦰")
st.title("माही: तुमची मैत्रीण 👩‍🦰")

# २. मॉडेल सेट करा
instruction = "तुझे नाव 'माही' आहे. तू युजरची एक जवळची मैत्रीण आहेस. तू मराठीत आपुलकीने बोलतेस."
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-latest", # 'latest' जोडून पहा
    system_instruction=instruction
)


# ३. चॅट हिस्ट्री
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []

# मेसेज दाखवण्यासाठी
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ४. युजर इनपुट
if prompt := st.chat_input("माहीशी बोला..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # माहीचे उत्तर
        response = st.session_state.chat.send_message(prompt)
        full_response = response.text
        
        with st.chat_message("assistant"):
            st.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
    except Exception as e:
        st.error(f"काहीतरी गडबड झाली: {e}")

