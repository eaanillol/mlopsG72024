import pandas as pd
from airflow import DAG
from datetime import datetime
from airflow.operators.python_operator import PythonOperator
from sqlalchemy import create_engine

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 3, 4)
}

def load_dataset():
    # Carga el conjunto de datos desde una fuente externa (por ejemplo, un archivo CSV)
    parent_directory = "/opt/airflow/datos/penguins_lter.csv"
    penguins = pd.read_csv(parent_directory)
    
    # Conexión a MySQL
    engine = create_engine('mysql://root:airflow@mysql:3306/penguin_data')
    
    # Guardar los datos en MySQL
    penguins.to_sql('penguins', con=engine, if_exists='replace', index=False)
    print("Datos cargados en MySQL")

with DAG(dag_id = 'data_loading_dag', 
         default_args=default_args, 
         schedule_interval=None) as dag:

     load_data_task = PythonOperator(task_id='load_dataset',
                                     python_callable=load_dataset)
     