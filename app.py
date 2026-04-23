
import streamlit as st
import google.generativeai as genai

# १. API Key Setup
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Secrets मध्ये API Key सापडली नाही!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.set_page_config(page_title="Mahi AI", page_icon="👩‍🦰")
st.title("माही: तुमची मैत्रीण 👩‍🦰")

# २. उपलब्ध मॉडेल शोधणे (Dynamic Model Selection)
@st.cache_resource
def get_working_model():
    # उपलब्ध मॉडेल्सची यादी मिळवा
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    # पसंतीची नावे (वेगवेगळ्या फॉरमॅटमध्ये)
    check_list = ['models/gemini-1.5-flash', 'models/gemini-pro', 'models/gemini-1.0-pro']
    
    for model_name in check_list:
        if model_name in available_models:
            return model_name
    
    # जर काहीच सापडले नाही तर यादीतील पहिले मॉडेल घ्या
    return available_models[0] if available_models else None

active_model_name = get_working_model()

if not active_model_name:
    st.error("तुमच्या API Key वर कोणतेही मॉडेल उपलब्ध नाही. कृपया Google AI Studio वर नवीन की तयार करा.")
    st.stop()

# ३. मॉडेल कॉन्फिगरेशन
instruction = "तुझे नाव माही आहे. तू एक जवळची मैत्रीण आहेस आणि मराठीत बोलतेस. तुला मागच्या गप्पा लक्षात राहतात."
model = genai.GenerativeModel(model_name=active_model_name, system_instruction=instruction)

# ४. मेमरी (Chat History) सेटअप
if "messages" not in st.session_state:
    st.session_state.messages = []

# आधीचे मेसेजेस दाखवा
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ५. युजर इनपुट
if prompt := st.chat_input("माहीशी बोला..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # चॅट सेशन सुरू करणे (Memory साठी)
        chat_session = model.start_chat(
            history=[
                {"role": "model" if m["role"] == "assistant" else "user", "parts": [m["content"]]}
                for m in st.session_state.messages[:-1]
            ]
        )
        
        response = chat_session.send_message(prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
    except Exception as e:
        st.error(f"काहीतरी गडबड झाली: {e}")






