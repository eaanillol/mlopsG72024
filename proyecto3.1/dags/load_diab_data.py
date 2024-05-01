from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from ucimlrepo import fetch_ucirepo
from airflow.sensors.time_delta import TimeDeltaSensor
from datetime import timedelta

def fetch_and_store():
    engine = create_engine('mysql+pymysql://root:airflow@mysql:3306/RAW_DATA')
    
    # Asegurar que la tabla batch_state exista y recuperar el último estado del batch
    with engine.connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS batch_state (
                id INT AUTO_INCREMENT PRIMARY KEY,
                last_index INT NOT NULL DEFAULT 0,
                batch_count INT NOT NULL DEFAULT 0
            );
        """)
        result = conn.execute("SELECT last_index, batch_count FROM batch_state LIMIT 1").fetchone()
        last_index, batch_count = (result['last_index'], result['batch_count']) if result else (0, 0)

    # Cargar y dividir los datos
    diabetes_130_us_hospitals_for_years_1999_2008 = fetch_ucirepo(id=296)
    X = diabetes_130_us_hospitals_for_years_1999_2008.data.features
    y = diabetes_130_us_hospitals_for_years_1999_2008.data.targets

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.25, random_state=42)

    # Almacenar los conjuntos de validación y test
    X_val.to_sql('diabetes_val', con=engine, if_exists='replace', index=False)
    X_test.to_sql('diabetes_test', con=engine, if_exists='replace', index=False)

    batch_size = 15000
    num_batches = 5
    indices = np.arange(len(X_train))

    # Calcular el nuevo índice
    new_index = last_index + batch_size
    if new_index >= len(indices):
        new_index = len(indices)
        batch_count += 1  # Incrementar el contador de batch

    # Extraer y preparar el batch de datos
    X_batch = X_train.iloc[last_index:new_index]

    # Guardar el nuevo batch en la base de datos
    X_batch.to_sql('diabetes_data', con=engine, if_exists='append', index=False)

    # Revisar el contador de batch y actuar según sea necesario
    if batch_count >1:
        with engine.connect() as conn:
            conn.execute("TRUNCATE TABLE diabetes_data")  # Limpiar los datos si se alcanza el límite de batch
            conn.execute("UPDATE batch_state SET last_index = 15000, batch_count = 0")
       
        # Extraer y preparar el batch de datos
        X_batch = X_train.iloc[0:15000]
        # Guardar el primer batch en la base de datos
        X_batch.to_sql('diabetes_data', con=engine, if_exists='replace', index=False)
   
    else:
        # Actualizar el estado del batch en la base de datos
        with engine.connect() as conn:
            if result:
                conn.execute("UPDATE batch_state SET last_index = %s, batch_count = %s", (new_index, batch_count))
            else:
                conn.execute("INSERT INTO batch_state (last_index, batch_count) VALUES (%s, %s)", (new_index, batch_count))

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 5, 1),
}

dag = DAG('diabetes_batch_processing', default_args=default_args, schedule_interval='@daily',concurrency=1)

t1 = PythonOperator(
    task_id='fetch_and_store_batch',
    python_callable=fetch_and_store,
    dag=dag,
    )

t1

