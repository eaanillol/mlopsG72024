# app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mlflow.pyfunc
import pandas as pd
import mlflow
from xgboost import XGBClassifier
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
    race: str = "AfricanAmerican"
    gender: str = "Female"
    age: str = "[70-80)"
    weight: str = "NULL"
    admission_type_id: int = 6
    discharge_disposition_id: int = 5
    admission_source_id: int = 17
    time_in_hospital: int = 5
    payer_code: str = "NULL"
    medical_specialty: str = "Orthopedics-Reconstructive"
    num_lab_procedures: int = 48
    num_procedures: int = 1
    num_medications: int = 22
    number_outpatient: int = 0
    number_emergency: int = 0
    number_inpatient: int = 0
    diag_1: str = "715"
    diag_2: str = "278"
    diag_3: str = "457"
    number_diagnoses: int = 6
    max_glu_serum: str = "None"
    A1Cresult: str = "None"
    metformin: str = "No"
    repaglinide: str = "No"
    nateglinide: str = "No"
    chlorpropamide: str = "No"
    glimepiride: str = "No"
    acetohexamide: str = "No"
    glipizide: str = "No"
    glyburide: str = "No"
    tolbutamide: str = "No"
    pioglitazone: str = "No"
    rosiglitazone: str = "No"
    acarbose: str = "No"
    miglitol: str = "No"
    troglitazone: str = "No"
    tolazamide: str = "No"
    examide: str = "No"
    citoglipton: str = "No"
    insulin: str = "No"
    glyburide_metformin: str = "No"  # Cambiado de glyburide-metformin
    glipizide_metformin: str = "No"  # Cambiado de glipizide-metformin
    glimepiride_pioglitazone: str = "No"  # Cambiado de glimepiride-pioglitazone
    metformin_rosiglitazone: str = "No"  # Cambiado de metformin-rosiglitazone
    metformin_pioglitazone: str = "No"  # Cambiado de metformin-pioglitazone
    change: str = "No"
    diabetesMed: str = "Yes"

#-------------------------------------------- preprocesamiento ------------------------------------------------------

# Limpiar los datos de entrada
def clean_data(data):
    # Eliminación de variables con una alta cantidad de valores nulos
    data.drop(['weight', 'payer_code', 'medical_specialty'], axis=1, inplace=True)

    # Eliminación de variables con un solo valor único
    data.drop(['examide', 'citoglipton', 'glimepiride-pioglitazone', 
               'acetohexamide', 'troglitazone'], axis=1, inplace=True)
    '''
    el objetivo del proyecto es: "to determine the early readmission of the patient within 30 days of discharge." por lo tanto,
    las variables correspondientes a pacientes sin registros de readmision o readmision despues de los 30 dias seran considerados
    como una variable unica.
    '''
    # Función para mapear los códigos a los capítulos
    def map_code_to_chapter(code):
        try:
            # Extracción del código numérico para diagnósticos estándar
            if code.startswith(('V', 'E')):
                if code.startswith('V'):
                    return 18  # Capítulo para códigos que comienzan con 'V'
                elif code.startswith('E'):
                    return 19  # Capítulo para códigos que comienzan con 'E'
            else:
                code_num = int(code.split('.')[0])  # Asumiendo que el código puede tener un formato decimal
                if 1 <= code_num <= 139:
                    return 1
                elif 140 <= code_num <= 239:
                    return 2
                elif 240 <= code_num <= 279:
                    return 3
                elif 280 <= code_num <= 289:
                    return 4
                elif 290 <= code_num <= 319:
                    return 5
                elif 320 <= code_num <= 389:
                    return 6
                elif 390 <= code_num <= 459:
                    return 7
                elif 460 <= code_num <= 519:
                    return 8
                elif 520 <= code_num <= 579:
                    return 9
                elif 580 <= code_num <= 629:
                    return 10
                elif 630 <= code_num <= 679:
                    return 11
                elif 680 <= code_num <= 709:
                    return 12
                elif 710 <= code_num <= 739:
                    return 13
                elif 740 <= code_num <= 759:
                    return 14
                elif 760 <= code_num <= 779:
                    return 15
                elif 780 <= code_num <= 799:
                    return 16
                elif 800 <= code_num <= 999:
                    return 17
                else:
                    return None  # Para códigos que no caen en ningún rango conocido
        except ValueError:
            return None  # En caso de que el código no sea convertible a entero
    # dado que no hay muchos valores faltantes en relacion al total, se eliminarán.
    data.dropna(subset=['diag_1','diag_2','diag_3'], inplace=True)
    # Aplicar la función de mapeo
    data['diag_class'] = data['diag_1'].apply(map_code_to_chapter)
    data['diag_2_class'] = data['diag_2'].apply(map_code_to_chapter)
    data['diag_3_class'] = data['diag_3'].apply(map_code_to_chapter)

    data.drop(['diag_1', 'diag_2', 'diag_3'], axis=1, inplace=True)

    # Convertir columnas numéricas
    # Lista de columnas numéricas según la descripción
    numeric_columns = [
        'time_in_hospital', 'num_lab_procedures', 'num_procedures', 
        'num_medications', 'number_outpatient', 'number_emergency', 
        'number_inpatient', 'number_diagnoses'
    ]

    # Convertir estas columnas a tipo numérico (float o int según sea necesario)
    for column in numeric_columns:
        data[column] = pd.to_numeric(data[column], errors='coerce')

    # Lista de columnas que son de tipo "object"
    object_columns = data.select_dtypes(include=['object']).columns

    # Convierte las columnas de tipo "object" a categorías
    data[object_columns] = data[object_columns].astype('category')
    data[["admission_type_id","discharge_disposition_id",'diag_2_class', 'diag_3_class',
        "admission_source_id","diag_class"]] = data[["admission_type_id","discharge_disposition_id",
                                                     'diag_2_class',"admission_source_id", 
                                                     "diag_class",'diag_3_class']].astype('category')
    # en comparación al total de valores, la variable race no tiene valores faltantes, se eliminan estas entradas del dataset.
    data.dropna(subset=['race'], inplace=True)
    """
    Dado que la distribución de variables entre las 2 clases de readmitted es practicamente la misma, esto puede causar 
    problemas al clasificar el modelo, dado que estas variables no dan ningún aporte estadistico a la clasificación"
    """
    data.drop([ "max_glu_serum", "A1Cresult", "metformin", "repaglinide", "nateglinide", "chlorpropamide", "glimepiride",
                "glipizide", "glyburide", "tolbutamide", "pioglitazone", "rosiglitazone", "acarbose", "miglitol", "tolazamide",
                "insulin", "glyburide-metformin", "glipizide-metformin", "metformin-rosiglitazone", "metformin-pioglitazone",
                "change", "diabetesMed"], axis=1, inplace=True)

    print("Data processing completed.")
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

    engine = create_engine('mysql+pymysql://root:airflow@10.43.101.156:30082/RAW_DATA')
   
    try:
        model, version = load_model()
        columns = [ "race", "gender", "age", "weight", "admission_type_id",
   		 "discharge_disposition_id", "admission_source_id", "time_in_hospital",
  	 	 "payer_code", "medical_specialty", "num_lab_procedures", "num_procedures",
   		 "num_medications", "number_outpatient", "number_emergency", "number_inpatient",
   		 "diag_1", "diag_2", "diag_3", "number_diagnoses", "max_glu_serum", "A1Cresult",
   		 "metformin", "repaglinide", "nateglinide", "chlorpropamide", "glimepiride",
   		 "acetohexamide", "glipizide", "glyburide", "tolbutamide", "pioglitazone",
    	         "rosiglitazone", "acarbose", "miglitol", "troglitazone", "tolazamide", "examide",
   	 	 "citoglipton", "insulin", "glyburide-metformin", "glipizide-metformin",
   	 	 "glimepiride-pioglitazone", "metformin-rosiglitazone", "metformin-pioglitazone",
   		 "change", "diabetesMed"]

        # Convertir la entrada a dataframe de pandas, guardar datos en MySQL y limpiar los datos
        input_df = pd.DataFrame([input.dict()],columns = columns)
        input_df.to_sql('new_diabetes_data', con=engine, if_exists='append', index=False)
        input_df =clean_data(input_df) 

        # Realizar la predicción
        prediction = model.predict(input_df)
       
        # Devolver la predicción
        return {"Prediction":str(prediction[0]), "Model Version": str(version)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
