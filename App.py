
import os
import streamlit as st
import datetime
from dotenv import load_dotenv
from meldrx_fhir_client import FHIRClient

# Read .env file...
load_dotenv()
MELDRX_WORKSPACE_URL = os.environ.get("MELDRX_WORKSPACE_URL")
MELDRX_WORKSPACE_ID = MELDRX_WORKSPACE_URL.split("/")[-1]
MELDRX_CLIENT_ID = os.environ.get("MELDRX_CLIENT_ID")
MELDRX_CLIENT_SECRET = os.environ.get("MELDRX_CLIENT_SECRET")

# Configuration...
MELDRX_BASE_URL = "https://app.meldrx.com"
SCOPE = "patient/*.read"

# Search for patients by name/dob...
def search_patients(first_name, last_name, dob):
    fhir = FHIRClient.for_client_secret(MELDRX_BASE_URL, MELDRX_WORKSPACE_ID, MELDRX_CLIENT_ID, MELDRX_CLIENT_SECRET, SCOPE)

    search_params = {}
    if first_name != "":
        search_params["given"] = first_name
    if last_name != "":
        search_params["family"] = last_name
    if dob != "":
        search_params["birthdate"] = dob

    # Search patients...
    return fhir.search_resource("Patient", search_params)


def render():
    # App Header...

    st.title("## Heart Attack Risk Prediction")
    st.markdown("___")

    # Search for Patient (first name, last name, birthdate)...
    st.markdown("## Search for Patient")
    search_first_name = st.text_input("First Name")
    search_last_name = st.text_input("Last Name")
    search_dob = st.text_input("Date of Birth (YYYY-MM-DD)")

    if st.button("Search"):
        search_results = search_patients(search_first_name, search_last_name, search_dob)

        # If no entries, display message and return...
        if "entry" not in search_results or len(search_results["entry"]) == 0 or search_results["entry"][0]['resource']['resourceType'] != 'Patient':
            st.markdown("No patients found.")
            return

        st.session_state['patient'] = search_results["entry"][0]["resource"]

    if 'patient' not in st.session_state:
        return

    patient = st.session_state['patient']

    name = patient["name"][0]["given"][0] + " " + patient["name"][0]["family"]
    gender = patient["gender"]
    dob = patient["birthDate"]
    age = datetime.datetime.now().year - int(dob[0:4])

    st.markdown("___")
    st.markdown("## Patient Data")
    st.markdown("Name: " + name)
    st.markdown("Gender: " + gender)
    st.markdown("Age: " + str(age))
    st.markdown("___")

    # Input fields, initialized with patient data (if possible)...
    gender = st.selectbox("Gender", ("Male", "Female"), 1 if gender == "female" else 0)
    age = st.number_input("Age (years)", min_value=0, max_value=150, value=age, step=1)
    weight = st.number_input("Weight (kg)", min_value=1.0, max_value=300.0, value=70.0, step=0.1)
    serum_creatinine = st.number_input("Serum Creatinine (umol/L)", min_value=0.1, max_value=1500.0, value=60.0, step=0.1)
    gender = st.selectbox("Gender", ("Male", "Female"), 1 if gender == "female" else 0)

    cp = st.selectbox('Chest Pain Type', ['Typical Angina', 'Atypical Angina', 'Non-anginal Pain', 'Asymptomatic'])
    trtbps = st.number_input('Resting Blood Pressure (mm Hg)', min_value=80, max_value=200, value=120)
    chol = st.number_input('Cholesterol (mg/dl)', min_value=100, max_value=600, value=200)
    fbs = st.selectbox('Fasting Blood Sugar > 120 mg/dl', ['Yes', 'No'])
    restecg = st.selectbox('Resting ECG', ['Normal', 'ST-T wave abnormality', 'Left ventricular hypertrophy'])
    thalachh = st.number_input('Maximum Heart Rate Achieved', min_value=60, max_value=220, value=150)
    exng = st.selectbox('Exercise Induced Angina', ['Yes', 'No'])
    oldpeak = st.number_input('ST depression induced by exercise relative to rest', min_value=0.0, max_value=6.2, value=1.0)
    slp = st.selectbox('Slope of the peak exercise ST segment', ['Upsloping', 'Flat', 'Downsloping'])
    caa = st.number_input('Number of major vessels (0-3) colored by flourosopy', min_value=0, max_value=3, value=0)
    thall = st.selectbox('Thalassemia', ['Normal', 'Fixed Defect', 'Reversable Defect'])
   

  # Heart Attack Risk Prediction section
    st.markdown("## Heart Attack Risk Prediction")
    if st.button("Predict Heart Attack Risk"):
        risk = heart_attack_risk(patient)
        if risk is not None:  # Check if prediction was successful
            if risk == 1:
                st.write("The patient is at risk of a heart attack.")
            else:
                st.write("The patient is not at risk of a heart attack.")
