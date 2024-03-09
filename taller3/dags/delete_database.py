from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from sqlalchemy import create_engine, inspect

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 3, 4)
}

def delete_data():
    # Conexión a la base de datos utilizando SQLAlchemy
    engine = create_engine('mysql://root:airflow@mysql:3306/penguin_data')
    
    # Crear un objeto inspector
    inspector = inspect(engine)
 #   # Borrar contenido de la tabla penguins
 #   with engine.connect() as connection:
 #       result = connection.execute("DELETE FROM penguins")
    # Verificar si la tabla 'penguins' existe en la base de datos
    if 'penguins' in inspector.get_table_names():
        # Ejecutar la consulta para eliminar la tabla 'penguins'
        engine.execute("DROP TABLE penguins")
        print("Tabla 'penguins' eliminada exitosamente.")
    else:
        print("La tabla 'penguins' no existe en la base de datos.")


with DAG(
    'delete_data_dag',
    default_args=default_args,
    description='DAG para borrar contenido de la base de datos',
    schedule_interval=None,
) as dag:

    delete_task = PythonOperator(
        task_id='delete_data_task',
        python_callable=delete_data,
    )
    