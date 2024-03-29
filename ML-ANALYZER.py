import streamlit as st
from code.DiseaseModel import DiseaseModel  # Ensure the correct import path
from code.helper import prepare_symptoms_array  # Ensure the correct import path
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import requests

st.set_page_config(
    page_title="ML-ANALYZER",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

st.markdown("""
    <nav class="navbar fixed-top navbar-expand navbar-dark" style="position: fixed; top: 0; left: 0; width: 100%; display: flex; justify-content: space-between; padding: 0.4rem; background-color: rgba(76,68,182); color: white;">
        <div class="collapse navbar-collapse justify-content-center align-items-center " id="navbarNav">
            <ul class="navbar-nav ">
                <li class="nav-item active" style="margin-right: 45rem; font-size: 1.2rem;">
                    <a class="nav-link " href="#"><b> ML-Analyzer </b><span class="sr-only">(current)</span></a>
                </li>
                 <li>
                    <div>
                        <a href="https://hdaanalyzer.000webhostapp.com/ml-analyzer.php" target="_self"><button style="background-color: #fff; color: #443e85; padding: 0.5rem 1rem; border: none; cursor: pointer; border-radius: 1rem; margin-top: 3px;">Close</button></a>
                    </div>
                </li>
            </ul>
        </div>
    </nav>
""", unsafe_allow_html=True)



    

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



def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()





lottie_coding = load_lottieurl("https://lottie.host/e8cca356-1ed3-4d6d-a263-377ffdbfae98/L1n9J2mGso.json")  # replace link to local lottie file



with st.sidebar:   
    selected = option_menu('',['ML-ANALYZER'],
                          icons=['person'],
                          default_index=0,
                          
                          )
    st_lottie(
                           lottie_coding,
                           speed=1,
                           reverse=False,
                           loop=True,
                           quality="low", # medium ; high
                           height="250px",
                           width="250px",
                           key=None,
                           )
        


code = """
"https://multiplediseasedetector.streamlit.app/"
"""

# Display the code in the sidebar using markdown
st.sidebar.markdown("```python\n{}\n```".format(code))

# Execute the code and display its output in the sidebar
with st.sidebar:
    exec(code)


# Create disease class and load ML model
disease_model = DiseaseModel()
disease_model.load_xgboost('model/xgboost_model.json')  # Replace with the correct model path


st.title('')
# Streamlit App Title
st.markdown("")
st.markdown("<h1 style='text-align: center;'>Disease Prediction using ML (Machine Learning)</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Choose the Symptoms That Describe Your Current Condition And Get The Appropriate Result</p>", unsafe_allow_html=True)
st.markdown("")

model = st.selectbox("Machine Learning Model", ("Xgboost-model",))
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


