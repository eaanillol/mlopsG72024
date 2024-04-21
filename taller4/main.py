# app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mlflow.pyfunc
import pandas as pd

app = FastAPI()

MLFLOW_TRACKING_URI = "http://mlflow_serv_t4:5000"
#MLFLOW_TRACKING_URI = "http://localhost:5000"
MODEL_NAME = "cover_type_class"

# Definir el modelo de entrada
class ModelInput(BaseModel):
    # Aquí debes definir las características de entrada que espera el modelo.
    Elevation: int = 2596
    Aspect: int = 51
    Slope: int = 3
    Horizontal_Distance_To_Hydrology: int =  258
    Vertical_Distance_To_Hydrology: int  = 0
    Horizontal_Distance_To_Roadways: int = 510
    Hillshade_9am: int = 211
    Hillshade_Noon: int = 232
    Hillshade_3pm: int = 148
    Horizontal_Distance_To_Fire_Points: int =  6279
    Wilderness_Area: str =" Rawah"
    Soil_Type: str =" C7745"

# Cargar el modelo de MLflow
def load_model():
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

    client = mlflow.tracking.MlflowClient()
    latest_versions = client.search_model_versions("name='cover_type_class'")

    if not latest_versions:
        raise ValueError(f"No se encontraron versiones para el modelo:cover_type_class")

    # Ordenar las versiones por tiempo de creación y tomar la última
    latest_version = sorted(latest_versions, key=lambda x: x.creation_timestamp, reverse=True)[0]

    model_uri = f"models:/cover_type_class/{latest_version.version}"
    model = mlflow.pyfunc.load_model(model_uri)
    return model,latest_version.version

@app.post("/predict")
def predict(input: ModelInput):
    try:
        model, version = load_model()
        columns = [
            "Elevation", "Aspect", "Slope",
            "Horizontal_Distance_To_Hydrology", "Vertical_Distance_To_Hydrology",
            "Horizontal_Distance_To_Roadways", "Hillshade_9am", "Hillshade_Noon",
            "Hillshade_3pm", "Horizontal_Distance_To_Fire_Points", "Wilderness_Area",
            "Soil_Type"
        ]
        # Convertir la entrada a dataframe de pandas
        input_df = pd.DataFrame([input.dict()],columns = columns)

        # Realizar la predicción
        prediction = model.predict(input_df)

        # Devolver la predicción
        return {"Prediction": prediction[0], "Model Version": version}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
