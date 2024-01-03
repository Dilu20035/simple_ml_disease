import streamlit as st
from streamlit_chat import message
import openai
import toml


st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

st.markdown("""
<nav class="navbar fixed-top navbar-expand navbar-dark" style="position: fixed; top: 0; left: 0; width: 100%; display: flex; justify-content: space-between; padding: 0.4rem; background-color: rgba(76,68,182,0.808); color: white;">
    <div class="collapse navbar-collapse justify-content-center align-items-center " id="navbarNav">
        <ul class="navbar-nav ">
            <li class="nav-item active" style="margin-right: 45rem; font-size: 1.2rem;">
                <a class="nav-link " href="#"><b> Medical Chatbot </b><span class="sr-only">(current)</span></a>
            </li>
            <li>
                <div>
                    <a href="https://chat.openai.com/c/12b8e7b5-491e-4353-b86b-af4e62c02fc6" target="_self"><button style="background-color: #fff; color: #443e85; padding: 0.5rem 1rem; border: none; cursor: pointer; border-radius: 1rem; margin-top: 3px;">Close</button></a>
                </div>
            </li>
        </ul>
    </div>
</nav>


""", unsafe_allow_html=True)

#<li class="nav-item">
#                <a class="nav-link" href="https://youtube.com/dataprofessor" target="_blank">YouTube</a>
#            </li>

    

# Set the theme colors
st.markdown(
    """
    <style>
    :root {
        --primary-color: #B21F33;
        --background-color: 002b36;
        --secondary-background-color: #586e75;
        --text-color: #fafafa;
        --font: sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)        


reduce_header_height_style = """
    <style>
        div.block-container {padding-top:0rem;}
    </style>
"""
st.markdown(reduce_header_height_style, unsafe_allow_html=True)




hide_st_style = """
            <style>
            #MainMenu {visibility: visible;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

secrets = toml.load("secrets.toml")
openai.api_key = secrets["openai"]["api_key"]

def get_initial_message():
    messages=[
            {"role": "system", "content": "You are a helpful Medical Diagnostic AI Doctor. Who anwers brief questions about Diseases, Symptomps and medical findings."},
            {"role": "user", "content": "I want to know about my disease"},
            {"role": "assistant", "content": "Thats awesome, what do you want to know about medical conditions"}
        ]
    return messages

def get_chatgpt_response(messages, model="gpt-3.5-turbo"):
    print("model: ", model)
    response = openai.ChatCompletion.create(
    model=model,
    messages=messages
    )
    return  response['choices'][0]['message']['content']

def update_chat(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages
# Function to update and display response
def update_and_display_response(query, model):
    messages = st.session_state['messages']
    messages = update_chat(messages, "user", query)
    response = get_chatgpt_response(messages, model)
    messages = update_chat(messages, "assistant", response)
    st.session_state.past.append(query)
    st.session_state.generated.append(response)

# Function to display chat history
def display_chat_history():
    for i in range(len(st.session_state['generated']) - 1, -1, -1):
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        message(st.session_state["generated"][i], key=str(i))


st.markdown("<h1 style='text-align: center;'>Medical Chatbot</h1>", unsafe_allow_html=True)
st.divider()

st.subheader("Ask Medical-Related Questions:")

# ChatGPT Model selection
model = st.selectbox("ChatGPT Model", ("gpt-3.5-turbo",))

# Initialize session state if not present
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'messages' not in st.session_state:
    st.session_state['messages'] = get_initial_message()

# Default medical prompt
query = st.text_input("Ask a medical question: ", key="input", value="What are the symptoms of a common cold?")

# Check if there's a default query and generate response on app start
if query and 'generated' not in st.session_state:
    update_and_display_response(query, model)

# Handle user input and generate response
if query:
    with st.spinner("Generating response..."):
        update_and_display_response(query, model)

# Display chat history
if st.session_state['generated']:
    display_chat_history()
