import joblib
import numpy as np
import pandas as pd
from airflow import DAG
from sklearn.svm import SVC
from datetime import datetime
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import KNNImputer, SimpleImputer
from sklearn.model_selection import train_test_split
from airflow.operators.python_operator import PythonOperator
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from airflow.sensors.external_task_sensor import ExternalTaskSensor
from sqlalchemy import create_engine

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 3, 4),
}

def train_model():
    # Conexión a la base de datos MySQL
    engine = create_engine('mysql://root:airflow@mysql:3306/penguin_data')
    
    # Consulta para cargar los datos desde la tabla en la base de datos
    query = "SELECT * FROM penguins"
    
    # Leer los datos desde MySQL
    penguins = pd.read_sql(query, con=engine)

    # Eliminar columnas no deseadas
    penguins.drop(['studyName','Sample Number','Region','Island','Stage','Individual ID','Clutch Completion',
                   'Date Egg', 'Comments'], axis=1, inplace=True)

    # Reemplazar valores '.' por NaN
    penguins.replace(".", np.nan, inplace=True)

    # Convertir las columnas 'Sex' y 'Species' a tipo categórico
    penguins[['Sex', 'Species']] = penguins[['Sex', 'Species']].astype('category')

    # Dividir los datos en características (X) y etiquetas (y)
    X = penguins.drop(columns='Species')
    y = penguins['Species']

    # Dividir los datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=54)

    # Preprocesamiento de datos
    numeric_transformer = Pipeline(steps=[
        ("imputer", KNNImputer(n_neighbors=15)), 
        ("scaler", StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent', missing_values=np.nan)),
        ('onehot', OneHotEncoder(drop='first'))
    ])

    preprocessor = ColumnTransformer(transformers=[
        ("num", numeric_transformer, X.select_dtypes(exclude="category").columns),
        ("cat", categorical_transformer, X.select_dtypes(include="category").columns)
    ])

    # Definir el modelo SVM
    clf = Pipeline(steps=[
        ("preprocessor", preprocessor), 
        ("SVM", SVC())
    ])

    # Entrenar el modelo SVM
    clf.fit(X_train, y_train)

    # Guardar el modelo entrenado
    joblib.dump(clf, 'SVM_model.joblib')

# Crear el DAG
dag = DAG('svm_training_dag', default_args=default_args, schedule_interval=None)

# Sensor para esperar a que la tarea del DAG de carga de datos termine con éxito
wait_for_data_loading = ExternalTaskSensor(
    task_id='wait_for_data_loading',
    external_dag_id='data_loading_dag',
    external_task_id='load_dataset',
    dag=dag
)

# Tarea para entrenar el modelo SVM
train_model_task = PythonOperator(
    task_id='train_model',
    python_callable=train_model,
    dag=dag
)

# Establecer la dependencia entre el sensor y la tarea de entrenamiento del modelo
wait_for_data_loading >> train_model_task
