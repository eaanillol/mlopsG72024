# app/main.py
from datetime import date
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mlflow.pyfunc
import pandas as pd
import mlflow
from xgboost import XGBRegressor
import numpy as np
from sqlalchemy import create_engine, text
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, FunctionTransformer

app = FastAPI()

MLFLOW_TRACKING_URI = "http://10.43.101.156:8084"
MODEL_NAME = "model_experiment"

# Definir el modelo de entrada
class ModelInput(BaseModel):
    brokered_by: str = "NULL"
    status: str = "for_sale"
    price: float = 289900
    bed: int = 4
    bath: float = 2
    acre_lot: float = 0.38
    street: int = 1758218
    city: str = "East Windsor"
    state: str = "Connecticut"
    zip_code: int = 6016
    house_size: int = 1617
    prev_sold_date: date = date(1999, 9, 30)

#-------------------------------------------- preprocesamiento ------------------------------------------------------

# Limpiar los datos de entrada
def clean_data(data):
    # Eliminación de variables categoricos con muchas clases y la fecha, que no aporta al modelo
    data.drop([" brokered_by", "street","zip_code", "city","status", "prev_sold_date"],axis=1,inplace=True)
    data["state"] = data["state"].astype('category')
    price_data = data['price']
    # Filtrar el DataFrame para excluir los valores en el rango de 0 a 1000
    data = data[~((price_data >= 0) & (price_data <= 1000))]
    return data

# Cargar el modelo de MLflow que está en producción y obtener su versión
def load_model():
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

    client = mlflow.tracking.MlflowClient()
    model_name = "model_experiment"

    # Obtener todas las versiones del modelo
    model_versions = client.search_model_versions(f"name='{model_name}'")

    # Filtrar para encontrar la versión en producción
    production_versions = [mv for mv in model_versions if mv.current_stage == 'Production']

    if not production_versions:
        raise ValueError(f"No se encontró la versión en producción para el modelo: {model_name}")

    # Suponiendo que solo hay una versión en producción a la vez
    production_version = production_versions[0]

    # Construir el URI del modelo
    model_uri = f"models:/{model_name}/{production_version.version}"
    model = mlflow.pyfunc.load_model(model_uri)

    print(f"Cargado modelo {model_name} versión {production_version.version} desde MLflow")
    return model, production_version.version

#--------------------------------------------API----------------------------------------------------------------------
@app.post("/predict")
def predict(input: ModelInput):

    engine = create_engine('mysql+pymysql://root:airflow@10.43.101.156:8082/RAW_DATA')
   
    try:
        model, version = load_model()
        columns = [" brokered_by", "status", "price", "bed", "bath", "acre_lot", 
		   "street", "city", "state", "zip_code", "house_size", "prev_sold_date"]

        # Convertir la entrada a dataframe de pandas, guardar datos en MySQL y limpiar los datos
        input_df = pd.DataFrame([input.dict()],columns = columns)
        input_df.to_sql('new_real_estate', con=engine, if_exists='append', index=False)
        input_df =clean_data(input_df) 

        # Realizar la predicción
        prediction = model.predict(input_df)
       
        # Devolver la predicción
        return {"Prediction":str(prediction[0]), "Model Version": str(version)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
