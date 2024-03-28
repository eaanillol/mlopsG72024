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
from airflow import DAG
from sklearn.svm import SVC
from datetime import datetime
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.impute import KNNImputer, SimpleImputer
from airflow.operators.python_operator import PythonOperator
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split, GridSearchCV
from airflow.sensors.external_task_sensor import ExternalTaskSensor
from sqlalchemy import create_engine


os.environ['MLFLOW_S3_ENDPOINT_URL'] = "http://10.43.101.156:8081"
os.environ['AWS_ACCESS_KEY_ID'] = 'admin'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'supersecret'

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 3, 4),
}
# Definir los nombres de las columnas
def model_train(df):
    
    # Conexión a la base de datos MySQL
    engine = create_engine('mysql://root:airflow@mysql:8082/cover_type')
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
    
    with mlflow.start_run(run_name="test_1") as run:
        # Definir el modelo SVM
        clf = Pipeline(steps=[
            ("preprocessor", preprocessor), 
            ("SVM", SVC())
        ])
    
        # Entrenar el modelo SVM
        clf.fit(X_train, y_train)
        score = clf.score(X_test, y_test)
        # Log de métricas
        mlflow.log_metric("accuracy", score)
        # Log del modelo
        mlflow.sklearn.log_model(clf, "model")
        
    y_pred=clf.predict(X_test)
    cm=skm.metrics.confusion_matrix(y_test,y_pred)
    plt.rcParams.update({'font.size': 16})
    cm_display = ConfusionMatrixDisplay(cm)
    cm_display = cm_display.plot(cmap=plt.cm.Oranges)
    return print("trained succesfully")
    

# Crear el DAG
dag = DAG('svm_training_dag', default_args=default_args, schedule_interval=None)

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

