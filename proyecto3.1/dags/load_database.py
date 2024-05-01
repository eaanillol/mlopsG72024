# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 22:04:39 2024

@author: crist
"""

import requests
import pandas as pd
from time import sleep
from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator
from sqlalchemy import create_engine

def pausa():
    sleep(360)  # 360 segundos equivalen a 6 minutos

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 4, 5),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def load_dataset():
    # Carga el conjunto de datos desde una fuente externa
    parent_directory = 'http://10.43.101.149/data?group_number=7'
    #Realiza la solicitud GET a la API
    response = requests.get(parent_directory)
    
    # Verifica si la solicitud fue exitosa
    if response.status_code == 200:
        # Convierte la respuesta en formato JSON a un objeto Python
        data = response.json()

        # Definir los nombres de las columnas
        column_names = [
            "Elevation", "Aspect", "Slope",
            "Horizontal_Distance_To_Hydrology", "Vertical_Distance_To_Hydrology",
            "Horizontal_Distance_To_Roadways", "Hillshade_9am", "Hillshade_Noon",
            "Hillshade_3pm", "Horizontal_Distance_To_Fire_Points", "Wilderness_Area",
            "Soil_Type", "Cover_Type"
        ]
        
        # Crear el DataFrame
        cover_type = pd.DataFrame(data["data"],columns = column_names)
            
        # Conexión a MySQL
        engine = create_engine('mysql://root:airflow@mysql:3306/cover_type')
        
        # Guardar los datos en MySQL
        cover_type.to_sql('cover_type', con=engine, if_exists='append', index=False)
        return print("Datos cargados en MySQL")   
    else:
        return print(f"Error al solicitar datos: {response.status_code}")
        
    
with DAG(dag_id = 'data_loading_dag', 
         default_args=default_args, 
         schedule_interval=timedelta(days=1),
         catchup= True) as dag:

         retraso = PythonOperator(
                                  task_id ="min_delay_6",
                                  python_callable =pausa,
                                 )
         load_data_task = PythonOperator(task_id='load_dataset',
                                     python_callable=load_dataset)
     
retraso >> load_data_task