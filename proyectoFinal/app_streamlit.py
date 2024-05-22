import streamlit as st
import requests
import pandas as pd

# URL de tu API FastAPI
API_URL = "http://10.43.101.156:8085/predict"

# Diseñar la interfaz de usuario
st.title("Predicción del Tipo de Cobertura del Suelo")

# Configuración de URLs para servicios
url_fastapi = "http://10.43.101.156:8085/docs"
url_mlflow = "http://10.43.101.156:8084"
url_airflow = "http://10.43.101.156:8080"
url_minio = "http://10.43.101.156:8083"
url_adminer = "http://10.43.101.156:8081/"

# Sección de enlaces a herramientas
st.markdown("### Enlaces a Herramientas")
st.markdown(f"""
- **FastAPI Documentation**: [Acceder]({url_fastapi})
- **MLflow Tracking UI**: [Acceder]({url_mlflow})
- **Airflow Webserver**: [Acceder]({url_airflow})
- **MinIO Browser**: [Acceder]({url_minio})
- **Adminer MySQL**: [Acceder]({url_adminer})
""")

# Crear campos para recibir la entrada del usuario
col1, col2, col3 = st.columns(3)

with col1:
    race = st.text_input("Race", value="AfricanAmerican")
    gender = st.text_input("Gender", value="Female")
    age = st.text_input("Age", value="[70-80)")
    weight = st.text_input("Weight", value="NULL")
    admission_type_id = st.number_input("Admission Type ID", value=6)
    discharge_disposition_id = st.number_input("Discharge Disposition ID", value=5)
    admission_source_id = st.number_input("Admission Source ID", value=17)
    time_in_hospital = st.number_input("Time in Hospital", value=5)
    payer_code = st.text_input("Payer Code", value="NULL")
    medical_specialty = st.text_input("Medical Specialty", value="Orthopedics-Reconstructive")
    num_lab_procedures = st.number_input("Number of Lab Procedures", value=48)
    num_procedures = st.number_input("Number of Procedures", value=1)
    num_medications = st.number_input("Number of Medications", value=22)

with col2:
    number_outpatient = st.number_input("Number of Outpatient Visits", value=0)
    number_emergency = st.number_input("Number of Emergency Visits", value=0)
    number_inpatient = st.number_input("Number of Inpatient Visits", value=0)
    diag_1 = st.text_input("Diag 1", value="715")
    diag_2 = st.text_input("Diag 2", value="278")
    diag_3 = st.text_input("Diag 3", value="457")
    number_diagnoses = st.number_input("Number of Diagnoses", value=6)
    max_glu_serum = st.text_input("Max Glu Serum", value="None")
    A1Cresult = st.text_input("A1C Result", value="None")
    metformin = st.text_input("Metformin", value="No")
    repaglinide = st.text_input("Repaglinide", value="No")
    nateglinide = st.text_input("Nateglinide", value="No")
    chlorpropamide = st.text_input("Chlorpropamide", value="No")

with col3:
    glimepiride = st.text_input("Glimepiride", value="No")
    acetohexamide = st.text_input("Acetohexamide", value="No")
    glipizide = st.text_input("Glipizide", value="No")
    glyburide = st.text_input("Glyburide", value="No")
    tolbutamide = st.text_input("Tolbutamide", value="No")
    pioglitazone = st.text_input("Pioglitazone", value="No")
    rosiglitazone = st.text_input("Rosiglitazone", value="No")
    acarbose = st.text_input("Acarbose", value="No")
    miglitol = st.text_input("Miglitol", value="No")
    troglitazone = st.text_input("Troglitazone", value="No")
    tolazamide = st.text_input("Tolazamide", value="No")
    examide = st.text_input("Examide", value="No")
    citoglipton = st.text_input("Citoglipton", value="No")
    insulin = st.text_input("Insulin", value="No")
    glyburide_metformin = st.text_input("Glyburide-Metformin", value="No")
    glipizide_metformin = st.text_input("Glipizide-Metformin", value="No")
    glimepiride_pioglitazone = st.text_input("Glimepiride-Pioglitazone", value="No")
    metformin_rosiglitazone = st.text_input("Metformin-Rosiglitazone", value="No")
    metformin_pioglitazone = st.text_input("Metformin-Pioglitazone", value="No")
    change = st.text_input("Change", value="No")
    diabetesMed = st.text_input("Diabetes Medication", value="Yes")

# Botón para realizar la predicción
if st.button("Predecir"):

    # Empaquetar la entrada en un diccionario
    input_dict = {
    "race": race,
    "gender": gender,
    "age": age,
    "weight": weight,
    "admission_type_id": admission_type_id,
    "discharge_disposition_id": discharge_disposition_id,
    "admission_source_id": admission_source_id,
    "time_in_hospital": time_in_hospital,
    "payer_code": payer_code,
    "medical_specialty": medical_specialty,
    "num_lab_procedures": num_lab_procedures,
    "num_procedures": num_procedures,
    "num_medications": num_medications,
    "number_outpatient": number_outpatient,
    "number_emergency": number_emergency,
    "number_inpatient": number_inpatient,
    "diag_1": diag_1,
    "diag_2": diag_2,
    "diag_3": diag_3,
    "number_diagnoses": number_diagnoses,
    "max_glu_serum": max_glu_serum,
    "A1Cresult": A1Cresult,
    "metformin": metformin,
    "repaglinide": repaglinide,
    "nateglinide": nateglinide,
    "chlorpropamide": chlorpropamide,
    "glimepiride": glimepiride,
    "acetohexamide": acetohexamide,
    "glipizide": glipizide,
    "glyburide": glyburide,
    "tolbutamide": tolbutamide,
    "pioglitazone": pioglitazone,
    "rosiglitazone": rosiglitazone,
    "acarbose": acarbose,
    "miglitol": miglitol,
    "troglitazone": troglitazone,
    "tolazamide": tolazamide,
    "examide": examide,
    "citoglipton": citoglipton,
    "insulin": insulin,
    "glyburide-metformin": glyburide_metformin,
    "glipizide-metformin": glipizide_metformin,
    "glimepiride-pioglitazone": glimepiride_pioglitazone,
    "metformin-rosiglitazone": metformin_rosiglitazone,
    "metformin-pioglitazone": metformin_pioglitazone,
    "change": change,
    "diabetesMed": diabetesMed}

    # Llamar a la API
    response = requests.post(API_URL, json=input_dict)
    
    if response.status_code == 200:
        prediction = response.json()["Prediction"]
        model_version = response.json()["Model Version"]
        st.success(f"La predicción es: {prediction}")
        st.write(f"Version del modelo: {model_version}")
    else:
        st.error("Error en la predicción")
