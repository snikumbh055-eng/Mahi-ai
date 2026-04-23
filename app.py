import streamlit as st
import google.generativeai as genai

# १. API Key Configuration
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Secrets मध्ये API Key सापडली नाही!")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.set_page_config(page_title="Mahi AI", page_icon="👩‍🦰")
st.title("माही: तुमची मैत्रीण 👩‍🦰")

# २. उपलब्ध मॉडेल्स शोधणे (Dynamic Model Selection)
@st.cache_resource
def load_model():
    # मॉडेल्सची यादी तपासा
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    # पसंतीचे मॉडेल्स क्रमाने तपासा
    preferred_models = ['models/gemini-1.5-flash', 'models/gemini-1.5-flash-latest', 'models/gemini-pro']
    
    for model_path in preferred_models:
        if model_path in available_models:
            return genai.GenerativeModel(model_path)
    
    # जर काहीच नाही सापडले तर जे उपलब्ध आहे ते पहिले मॉडेल घ्या
    if available_models:
        return genai.GenerativeModel(available_models[0])
    return None

model = load_model()

if model is None:
    st.error("तुमच्या API Key वर कोणतेही मॉडEL उपलब्ध नाही. कृपया नवीन API Key तयार करा.")
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
        # साधे उत्तर मिळवा
        full_prompt = f"Tu mazi maitrin Mahi aahes. Marathi madhe bol. Prashna: {prompt}"
        response = model.generate_content(full_prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"काहीतरी गडबड झाली: {e}")




