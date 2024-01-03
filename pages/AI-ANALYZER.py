import streamlit as st
import openai
import toml



st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

st.markdown("""
<nav class="navbar fixed-top navbar-expand navbar-dark" style="position: fixed; top: 0; left: 0; width: 100%; display: flex; justify-content: space-between; padding: 0.4rem; background-color: rgba(76,68,182,0.808); color: white;">
    <div class="collapse navbar-collapse justify-content-center align-items-center " id="navbarNav">
        <ul class="navbar-nav ">
            <li class="nav-item active" style="margin-right: 45rem; font-size: 1.2rem;">
                <a class="nav-link " href="#"><b> Medical Diagnostic AI-Analyzer </b><span class="sr-only">(current)</span></a>
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


# Set OpenAI API key
# Replace with your actual API key
secrets = toml.load("secrets.toml")
openai.api_key = secrets["openai"]["api_key"]


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
