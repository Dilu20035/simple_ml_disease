import streamlit as st
from code.DiseaseModel import DiseaseModel  # Ensure the correct import path
from code.helper import prepare_symptoms_array  # Ensure the correct import path

# Create disease class and load ML model
disease_model = DiseaseModel()
disease_model.load_xgboost('ML-DETECTOR/model/xgboost_model.json')  # Replace with the correct model path

# Set page width to wide
st.set_page_config(layout='wide')

# Create sidebar
st.sidebar.markdown('# Disease Prediction')
# ... (sidebar content)

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

    # Display description and precautions in tabs
    tab1, tab2= st.tabs(["Description", "Precautions"])

    with tab1:
        st.write(disease_model.describe_predicted_disease())

    with tab2:
        st.write('Precautions:')
        precautions = disease_model.predicted_disease_precautions()
        for i in range(4):
            st.write(f'{i+1}. {precautions[i]}')
