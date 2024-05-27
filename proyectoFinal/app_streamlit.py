from datetime import date
import streamlit as st
import requests
import pandas as pd

# URL de tu API FastAPI
API_URL = "http://10.43.101.156:8085/predict"

# Diseñar la interfaz de usuario
st.title("Predicción del precio de venta de un inmueble")

# Configuración de URLs para servicios
url_fastapi = "http://10.43.101.156:8085/docs"
url_mlflow = "http://10.43.101.156:8084"
url_airflow = "http://10.43.101.156:8080"
url_minio = "http://10.43.101.156:8083"
url_adminer = "http://10.43.101.156:8081/"
url_jupyter = "http://10.43.101.156:8087/"

# Sección de enlaces a herramientas
st.markdown("### Enlaces a Herramientas")
st.markdown(f"""
- **FastAPI Documentation**: [Acceder]({url_fastapi})
- **MLflow Tracking UI**: [Acceder]({url_mlflow})
- **Airflow Webserver**: [Acceder]({url_airflow})
- **MinIO Browser**: [Acceder]({url_minio})
- **Adminer MySQL**: [Acceder]({url_adminer})
- **Interpretación modelo en Jupyter**: [Acceder]({url_jupyter})
""")

# Crear campos para recibir la entrada del usuario
col1, col2, col3 = st.columns(3)

with col1:
    brokered_by = st.text_input("Brokered by", value="NULL")
    status = st.text_input("Status", value="for_sale")
    price = st.number_input("Price", value=289900)
    bed = st.number_input("Bedrooms", value=4)

with col2:
    bath = st.number_input("Bathrooms", value=2.0)
    acre_lot = st.number_input("Acre Lot", value=0.38, format="%.2f")
    street = st.number_input("Street Number", value=1758218)
    city = st.text_input("City", value="East Windsor")

with col3:
    state = st.text_input("State", value="Connecticut")
    zip_code = st.number_input("ZIP Code", value=6016)
    house_size = st.number_input("House Size (sq ft)", value=1617)
    prev_sold_date = st.date_input("Previous Sold Date", value=date(1999, 9, 30))

# Botón para realizar la predicción
if st.button("Predecir"):
    # Empaquetar la entrada en un diccionario
    input_dict = {
    " brokered_by": brokered_by,
    "status": status,
    "price": price,
    "bed": bed,
    "bath": bath,
    "acre_lot": acre_lot,
    "street": street,
    "city": city,
    "state": state,
    "zip_code": zip_code,
    "house_size": house_size,
    "prev_sold_date": prev_sold_date.isoformat(),  # Convertir a string en formato ISO,
    }

    # Llamar a la API
    response = requests.post(API_URL, json=input_dict)
    
    if response.status_code == 200:
        prediction = response.json()["Prediction"]
        model_version = response.json()["Model Version"]
        st.success(f"La predicción es: {prediction}")
        st.write(f"Version del modelo: {model_version}")
    else:
        st.error("Error en la predicción")
