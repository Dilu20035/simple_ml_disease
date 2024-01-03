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
    # Streamlit app title and description
    st.markdown("<h1 style='text-align: center;'>Medical Diagnostic AI-Analyzer</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Enter patient information to receive a diagnostic recommendation</p>", unsafe_allow_html=True)
    st.divider()
    
    
    col1, col2, col3 = st.columns(3, gap="large")
    
    # User inputs
    with col1:
        gender = st.radio("Gender", ["Male", "Female"])
    with col2:    
        pregnancy = st.radio("Pregnancy", ["No", "Yes"]) if gender == "Female" else "No"
    with col3:
        age = st.number_input("Age", min_value=0, max_value=99, step=1)
    
    context = st.text_input("Patient's Background *(Example: gone to an outdoor music festival in north america, shared drinks and cigarettes with friends with similar symptoms)*", placeholder="none", max_chars=500 ,help=":green[**Enter patient's known background information, including their past medical conditions, medications, family history, lifestyle, and other relevant information that can help in diagnosis and treatment**]")
    symptoms = st.text_input("Symptoms *(Example: high-grade fever, lethargy, headache, and abdominal pain for two days)*", placeholder="none", max_chars=500 ,help=":green[**List all symptoms indicating the presence of an underlying medical condition**]")
    exam_findings = st.text_input("Examination Findings *(Example: petechial lesions on the palms of his hands and feet, bug bites)*", placeholder="none", max_chars=500, help=":green[**List all the information gathered through visual inspection, palpation, percussion, and auscultation during the examination**]")
    lab_results = st.text_input("Laboratory Test Results *(Example: w/IgE levels > 3000 IU/m)*", placeholder="none", max_chars=500, help=":green[**List output of tests performed on samples of bodily fluids, tissues, or other substances to help diagnose, monitor, or treat medical conditions. These tests can include blood tests, urine tests, imaging tests, biopsies, and other diagnostic procedures**]")
    
    # Combine user inputs into a report
    report_list = [
        f"Gender: {gender}",
        f"Age: {age}",
        f"Pregnancy: {pregnancy}" if gender == "Female" else "",
        context,
        symptoms,
        exam_findings,
        lab_results
    ]
    report = "\n".join([f"{i + 1}. {report_list[i]}" for i in range(len(report_list)) if report_list[i] != "none"])
    
    # Button to trigger the diagnostic analysis
    if st.button("Analyze"):
        if symptoms != "none":
            # Add a spinner while generating the diagnostic recommendation
            with st.spinner("Generating diagnostic details..."):
                # Make API call to OpenAI
                response = openai.Completion.create(
                    engine="text-davinci-003",  # Use Codex engine for code-based tasks
                    prompt=f"Patient with the following information:\n\n{report}\n\nProvide diagnostic name, precautions and a large brief explanation about the found diagnostic.",
                    max_tokens=300
                )
    
            # Display the diagnostic recommendation
            st.subheader("Predicted Diagnostic Details:")
            st.write(response["choices"][0]["text"])
    
            # Display a note
            st.divider()
            st.info(
                "Disclaimer: The diagnostic recommendation provided here is generated based on the information provided "
                "and is not a substitute for professional medical advice. It is important to note that this system does not "
                "guarantee 100% accuracy. Consultation with a qualified healthcare professional is strongly recommended for "
                "a precise and reliable diagnosis. Your health and well-being are of utmost importance, and a medical expert "
                "can provide personalized guidance based on a thorough examination of your specific situation."
            )
            st.divider()
        else:
            st.warning("Please enter symptoms before analyzing.")
        
# Sidebar navigation
page = st.sidebar.selectbox("Select Page", ("Chatbot", "Disease Prediction", "Diagnostic Analyzer"))

# Show selected page based on sidebar selection
if page == "Chatbot":
    chatbot_page()
elif page == "Disease Prediction":
    disease_prediction_page()
elif page == "Diagnostic Analyzer":
    diagnostic_analyzer_page()
