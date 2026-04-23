import streamlit as st
import google.generativeai as genai

# १. API Key Configuration
if "GEMINI_API_KEY" not in st.secrets:
    st.error("API Key सापडली नाही! कृपया Secrets तपासा.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.set_page_config(page_title="Mahi AI", page_icon="👩‍🦰")
st.title("माही: तुमची मैत्रीण 👩‍🦰")

# २. मॉडेलची खात्री करा (gemini-1.5-flash न चालल्यास gemini-pro वापरू)
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
    # एक छोटा टेस्ट मेसेज पाठवून पाहूया
    test_response = model.generate_content("Hi")
except Exception:
    # जर वरील मॉडेल चालले नाही, तर हे जुने पण खात्रीशीर मॉडेल वापरू
    model = genai.GenerativeModel('gemini-pro')

# ३. चॅट इंटरफेस
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("माहीशी बोला..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # माहीचे उत्तर (System Instruction सोप्या भाषेत)
    full_prompt = f"Tu mazi maitrin Mahi aahes. Mazya prashnach uttar Marathi madhe de: {prompt}"
    response = model.generate_content(full_prompt)
    
    with st.chat_message("assistant"):
        st.markdown(response.text)
    st.session_state.messages.append({"role": "assistant", "content": response.text})


