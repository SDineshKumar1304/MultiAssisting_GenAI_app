import streamlit as st
import google.generativeai as genai
import base64

st.title("I am Your Code Assistant 🤓")
st.snow()
st.balloons()

if "memory" not in st.session_state:
    st.session_state["memory"] = []

@st.cache_data(persist=True)
def getImageAsBase64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img = getImageAsBase64("C:\\Users\\svani\\Downloads\\Data_Science_tutor\\blues.jpeg")

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

genai.configure(api_key=key)

instructions = """Consider You are the Best Code Reviewer and Debugger in the World,Your Task is to find the bugs and Explain how to Solve the bugs and also
                you Should Fix the Bugs,and explain Everything in the Polite and Professional way,You Need to Show the Debugging Steps Also in json format"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    system_instruction=instructions
)
chat = model.start_chat(history=st.session_state["memory"])

def show_chat_history(chat):
    for message in chat.history:
        sender = "AI" if message.role == "model" else "You"
        st.markdown(f'<p style="color:black;">{sender}: {message.parts[0].text}</p>', unsafe_allow_html=True)

st.markdown('<p style="color:black;">Hi there! How can I assist you today?</p>', unsafe_allow_html=True)

show_chat_history(chat)

user_input = st.text_area("🤓 ")

if st.button("Clear Chat"):
    st.session_state["memory"] = []
    st.experimental_rerun()

if user_input:
    st.markdown(f'<p style="color:black;">You: {user_input}</p>', unsafe_allow_html=True)
    try:
        response = chat.send_message(user_input)
        for bot in response:
            st.markdown(f'<p style="color:black;">AI: {bot.parts[0].text}</p>', unsafe_allow_html=True)
        st.session_state["memory"] = chat.history
    except genai.generation_types.StopCandidateException:
        st.markdown('<p style="color:black;">AI: I\'m sorry, I couldn\'t understand that. Can you please provide more specific information?</p>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
