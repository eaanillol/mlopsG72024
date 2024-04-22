# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 21:26:15 2024

@author: crist
"""
import os
import mlflow
import joblib
import numpy as np
import pandas as pd
import sklearn as skm
from scipy.stats import randint
from airflow import DAG
from sklearn.svm import SVC
from datetime import datetime,timedelta
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import KNNImputer, SimpleImputer
from airflow.operators.python_operator import PythonOperator
from sklearn.model_selection import RandomizedSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import precision_score, recall_score, f1_score
from airflow.sensors.external_task_sensor import ExternalTaskSensor
from sqlalchemy import create_engine



default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 4, 4),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),

}

def load_data():
    # Conexión a la base de datos MySQL
    engine = create_engine('mysql://root:airflow@mysql:3306/cover_type')
    # Consulta para cargar los datos desde la tabla en la base de datos
    query = "SELECT * FROM cover_type"
    # Leer los datos desde MySQL
    df = pd.read_sql(query, con=engine)
    # Convertir las columnas 'Sex' y 'Species' a tipo categórico
    df[['Wilderness_Area', 'Soil_Type','Cover_Type']] = df[['Wilderness_Area', 'Soil_Type','Cover_Type']].astype('category')
    # Dividir los datos en características (X) y etiquetas (y)
    X = df.drop(columns='Cover_Type')
    y = df['Cover_Type']
    # Dividir los datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=54) 
    return X_train, X_test, y_train, y_test

def model_train():
    X_train, X_test, y_train, y_test = load_data()
    # Conexión a la base de datos MySQL
    engine = create_engine('mysql://root:airflow@mysql:3306/cover_type')
    # Consulta para cargar los datos desde la tabla en la base de datos
    query = "SELECT * FROM cover_type"
    # Leer los datos desde MySQL
    df = pd.read_sql(query, con=engine)
    # Convertir las columnas 'Sex' y 'Species' a tipo categórico
    df[['Wilderness_Area', 'Soil_Type','Cover_Type']] = df[['Wilderness_Area', 'Soil_Type','Cover_Type']].astype('category')
    # Dividir los datos en características (X) y etiquetas (y)
    X = df.drop(columns='Cover_Type')
    y = df['Cover_Type']

    # Dividir los datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=54)

    # Preprocesamiento de datos
    numeric_transformer = Pipeline(steps=[
        ("imputer", KNNImputer(n_neighbors=15)), 
        ("scaler", StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent', missing_values=np.nan)),
        ('onehot', OneHotEncoder(drop='first',handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer(transformers=[
        ("num", numeric_transformer, X.select_dtypes(exclude="category").columns),
        ("cat", categorical_transformer, X.select_dtypes(include="category").columns)
    ])
    
    # connects to the Mlflow tracking server that you started above
    mlflow.set_tracking_uri("http://10.43.101.156:8081")
    mlflow.set_experiment("mlflow_tracking")
    with mlflow.start_run(run_name="cover_type_class") as run:
        mlflow.log_params(best_params)
        mlflow.log_metric("accuracy", random_search.best_score_)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1_score", f1)
        mlflow.sklearn.log_model(best_estimator, "model")
	# Registrar el modelo en MLflow Model Registry
        model_uri = f"runs:/{run.info.run_id}/model"
        model_details = mlflow.register_model(model_uri=model_uri, name="cover_type_class")

    print("Trained successfully.")
    

# Crear el DAG
dag = DAG('svm_training_dag', default_args=default_args, schedule_interval=timedelta(days=1), catchup= True)

# Sensor para esperar a que la tarea del DAG de carga de datos termine con éxito
"""wait_for_data_loading = ExternalTaskSensor(
    task_id='wait_for_data_loading',
    external_dag_id='data_loading_dag',
    external_task_id='load_dataset',
    dag=dag
)"""

# Tarea para entrenar el modelo SVM
train_model_task = PythonOperator(
    task_id='train_model',
    python_callable=model_train,
    dag=dag
)

# Establecer la dependencia entre el sensor y la tarea de entrenamiento del modelo
#wait_for_data_loading >> train_model_task

