import streamlit as st
import google.generativeai as genai

# १. API Key Setup
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Secrets मध्ये API Key सापडली नाही!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.set_page_config(page_title="Mahi AI", page_icon="👩‍🦰")
st.title("माही: तुमची मैत्रीण 👩‍🦰")

# २. उपलब्ध मॉडेल शोधणे
@st.cache_resource
def get_working_model():
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    check_list = ['models/gemini-1.5-flash', 'models/gemini-pro']
    for model_name in check_list:
        if model_name in available_models:
            return model_name
    return available_models[0] if available_models else None

active_model_name = get_working_model()

# ३. मॉडेल कॉन्फिगरेशन
instruction = "तुझे नाव माही आहे. तू एक जवळची मैत्रीण आहेस आणि मराठीत बोलतेस. तुला मागच्या गप्पा लक्षात राहतात."
model = genai.GenerativeModel(model_name=active_model_name, system_instruction=instruction)

# --- बदल येथे आहे: ४. मेमरी (Chat Session) सेटअप ---
# फक्त मेसेज साठवून उपयोगाचे नाही, पूर्ण 'chat_session' साठवावा लागतो
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# आधीचे मेसेजेस स्क्रीनवर दाखवण्यासाठी (UI साठी)
for message in st.session_state.chat_session.history:
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# ५. युजर इनपुट
if prompt := st.chat_input("माहीशी बोला..."):
    # स्क्रीनवर युजरचा मेसेज दाखवा
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # 'send_message' वापरल्याने Gemini स्वतःहून हिस्ट्री मॅनेज करतो
        response = st.session_state.chat_session.send_message(prompt)
        
        # एआयचे उत्तर दाखवा
        with st.chat_message("assistant"):
            st.markdown(response.text)
        
    except Exception as e:
        st.error(f"काहीतरी गडबड झाली: {e}")
        






