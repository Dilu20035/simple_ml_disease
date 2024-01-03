import streamlit as st
import openai
import toml
from code.DiseaseModel import DiseaseModel
from code.helper import prepare_symptoms_array
from streamlit_chat import message

# Set OpenAI API key
secrets = toml.load("secrets.toml")
openai.api_key = secrets["openai"]["api_key"]

# Initialize Streamlit app title and description
st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)
st.markdown("""
<nav class="navbar fixed-top navbar-expand navbar-dark" style="position: fixed; top: 0; left: 0; width: 100%; display: flex; justify-content: space-between; padding: 0.4rem; background-color: rgba(76,68,182,0.808); color: white;">
    <!-- Navigation menu -->
</nav>
""", unsafe_allow_html=True)

# Set the theme colors
st.markdown("""
    <style>
    :root {
        /* Theme colors */
    }
    </style>
    """, unsafe_allow_html=True)

# Define functions for different functionalities (Chatbot, Disease Prediction, Diagnostic Analyzer)

# Chatbot Functionality
def chatbot_page():
    # Chatbot code here

# Disease Prediction Functionality
def disease_prediction_page():    
    # Create disease class and load ML model
    disease_model = DiseaseModel()
    disease_model.load_xgboost('model/xgboost_model.json')  # Replace with the correct model path
    
    st.sidebar.write('Disease Prediction using Machine Learning')
    # Title
    st.write('# Disease Prediction using Machine Learning')
    
    # Get symptoms from user input
    symptoms = st.multiselect('What are your symptoms?', options=disease_model.all_symptoms)
    
    X = prepare_symptoms_array(symptoms)  # Assuming prepare_symptoms_array handles symptom data
    
    # Trigger XGBoost model
    if st.button('Predict'): 
        # Run the model prediction
        prediction, prob = disease_model.predict(X)  # Assuming predict() returns prediction and probability
        
        st.write(f'## Disease: {prediction} with {prob*100:.2f}% probability')
    
        st.write(disease_model.describe_predicted_disease())
        st.text("")
        st.write("## Precautions:")
        precautions = disease_model.predicted_disease_precautions()
        for i in range(4):
            st.write(f'{i+1}. {precautions[i]}')


# Diagnostic Analyzer Functionality
def diagnostic_analyzer_page():
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

# Sidebar navigation
page = st.sidebar.selectbox("Select Page", ("Chatbot", "Disease Prediction", "Diagnostic Analyzer"))

# Show selected page based on sidebar selection
if page == "Chatbot":
    chatbot_page()
elif page == "Disease Prediction":
    disease_prediction_page()
elif page == "Diagnostic Analyzer":
    diagnostic_analyzer_page()
