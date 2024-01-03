import streamlit as st
from code.DiseaseModel import DiseaseModel  # Ensure the correct import path
from code.helper import prepare_symptoms_array  # Ensure the correct import path

st.set_page_config(page_title="HDA-ML-Analyzer", page_icon=None, layout="centered", initial_sidebar_state="collapsed", menu_items=None)
st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

st.markdown("""
<nav class="navbar fixed-top navbar-expand navbar-dark" style="position: fixed; top: 0; left: 0; width: 100%; display: flex; justify-content: space-between; padding: 0.4rem; background-color: rgba(76,68,182,0.808); color: white;">
    <div class="collapse navbar-collapse justify-content-center align-items-center " id="navbarNav">
        <ul class="navbar-nav ">
            <li class="nav-item active" style="margin-right: 45rem; font-size: 1.2rem;">
                <a class="nav-link " href="#"><b> Medical Diagnostic ML-Analyzer </b><span class="sr-only">(current)</span></a>
            </li>
            <li>
                <div>
                    <button onclick="window.close()" style="background-color: #fff; color: #443e85; padding: 0.5rem 1rem; border: none; cursor: pointer; border-radius: 1rem; margin-top: 3px;">Close</button>
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




# Create disease class and load ML model
disease_model = DiseaseModel()
disease_model.load_xgboost('ML-DETECTOR/model/xgboost_model.json')  # Replace with the correct model path

# Set page width to wide
st.set_page_config(layout='centered')

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
