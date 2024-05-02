import streamlit as st
import google.generativeai as genai
import base64



st.title("I am your Lawyer ⚖️🧑‍⚖️")
st.snow()
st.balloons()


if "memory" not in st.session_state:
    st.session_state["memory"] = []


@st.cache_data(persist=True)
def getImageAsBase64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img = getImageAsBase64("C:\\Users\\svani\\Downloads\\Data_Science_tutor\\convo.png")

st.markdown(f"""
  <style>
    [data-testid="stAppViewContainer"]{{
      background-color: #ffffff; /* White background */
      background-image: url("data:image/png;base64,{img}");
      background-size: cover;
    }}
    .stApp h1, .stApp div[data-baseweb="card"] > div > div > div > div > div > div, .stApp div[class^="main"] > div > div > div > div > div > div > div {{
      color: #000000 !important; /* Black text */
    }}
    .stMarkdown, .stTextInput, .stTextArea, .stNumberInput, .stSlider, .stSelectbox, .stButton, .you-text {{
      color: #000000 !important; /* Black text */
    }}
  </style>""",unsafe_allow_html=True)


f = open('C:\\Users\\svani\\Downloads\\Data_Science_tutor\\keys\\DS.Key.txt')
key = f.read()

with open("C:\\Users\\svani\\Downloads\\Data_Science_tutor\\keys\\law.txt") as f:
    instructions = f.read()

genai.configure(api_key=key)


############################################################################
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    system_instruction=instructions
)

##########################################################################
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "Hii 🤖,  I'm here to help you"}
    ]
    st.title("I am Here to Clear Your Doubts")



##############################################################################
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input()

if user_input is not None:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Loading..."):
            ai_response = model.generate_content(user_input)
            st.write(ai_response.text)
    new_ai_message = {"role": "assistant", "content": ai_response.text}
    st.session_state.messages.append(new_ai_message)