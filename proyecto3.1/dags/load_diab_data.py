import mlflow
from airflow import DAG
from xgboost import XGBClassifier
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from ucimlrepo import fetch_ucirepo
from airflow.sensors.time_delta import TimeDeltaSensor
from datetime import timedelta
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, FunctionTransformer
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay


engine = create_engine('mysql+pymysql://root:airflow@10.43.101.156:30082/RAW_DATA')
engine_2 = create_engine('mysql+pymysql://root:airflow@10.43.101.156:30082/CLEAN_DATA')

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
    data['readmitted'] = data['readmitted'].replace({'>30': 0,'<30': 1,'NO': 0})
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

def fetch_and_store():
    
    
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
    print(y_val) 
    # Combina las características y los targets en un solo DataFrame para validación
    val_data = pd.concat([X_val, y_val], axis=1)
    clean_val_data = clean_data(val_data.copy()) 
    # Combina las características y los targets en un solo DataFrame para pruebas
    test_data = pd.concat([X_test,y_test], axis=1)
    clean_test_data = clean_data(test_data.copy()) 
    # Almacenar los conjuntos de validación y test
    val_data.to_sql('diabetes_val', con=engine, if_exists='replace', index=False)
    test_data.to_sql('diabetes_test', con=engine, if_exists='replace', index=False)
    clean_val_data.to_sql('diabetes_val', con=engine_2, if_exists='replace', index=False)
    clean_test_data.to_sql('diabetes_test', con=engine_2, if_exists='replace', index=False)
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
    y_batch = y_train.iloc[last_index:new_index]
    batch_data = pd.concat([X_batch,y_batch], axis=1)
    clean_batch_data = clean_data(batch_data.copy())
    # Guardar el nuevo batch en la base de datos
    batch_data.to_sql('diabetes_data', con=engine, if_exists='append', index=False)
    clean_batch_data.to_sql('diabetes_data', con=engine_2, if_exists='append', index=False)
    # Revisar el contador de batch y actuar según sea necesario
    if batch_count >1:
        with engine.connect() as conn:
            conn.execute("TRUNCATE TABLE diabetes_data")  # Limpiar los datos si se alcanza el límite de batch
            conn.execute("UPDATE batch_state SET last_index = 15000, batch_count = 0")
        with engine_2.connect() as conn_2:
            conn_2.execute("TRUNCATE TABLE diabetes_data")  # Limpiar los datos si se alcanza el límite de batch 
        # Extraer y preparar el batch de datos
        X_batch = X_train.iloc[0:15000]
        y_batch = y_train.iloc[0:15000]
        batch_data = pd.concat([X_batch,y_batch], axis=1)
        clean_batch_data = clean_data(batch_data.copy())
        # Guardar el nuevo batch en la base de datos
        batch_data.to_sql('diabetes_data', con=engine, if_exists='append', index=False) 
        clean_batch_data.to_sql('diabetes_data', con=engine_2, if_exists='append', index=False)      
   
    else:
        # Actualizar el estado del batch en la base de datos
        with engine.connect() as conn:
            if result:
                conn.execute("UPDATE batch_state SET last_index = %s, batch_count = %s", (new_index, batch_count))
            else:
                conn.execute("INSERT INTO batch_state (last_index, batch_count) VALUES (%s, %s)", (new_index, batch_count))

def model_train():
    # Crear una consulta SQL como un objeto de texto para ser ejecutado.
    query_A = text("SELECT * FROM diabetes_data")
    query_B = text("SELECT * FROM diabetes_val")
    query_C = text("SELECT * FROM diabetes_test")

    # Ejecuta la consulta y carga los datos en un DataFrame de pandas
    train_data = pd.read_sql(query_A, engine_2.connect())
    validation_data = pd.read_sql(query_B, engine_2.connect())
    test_data = pd.read_sql(query_C, engine_2.connect())
    # Separar características y etiquetas para el conjunto de entrenamiento
    X_train = train_data.drop('readmitted', axis=1)
    y_train = train_data['readmitted']

    # Separar características y etiquetas para el conjunto de prueba
    X_test = test_data.drop('readmitted', axis=1)
    y_test = test_data['readmitted']

    # Separar características y etiquetas para el conjunto de validación
    X_validation = validation_data.drop('readmitted', axis=1)
    y_validation = validation_data['readmitted']
    # Definición del transformer numérico
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='mean')),  # Imputa valores faltantes con la media
        ('scaler', StandardScaler())                 # Escala los datos
    ])

    # Función para convertir columnas object a category
    def convert_to_category(X):
        for col in X.columns:
            X[col] = X[col].astype('category')
        return X

    # Transformador para cambiar el tipo de datos
    category_converter = FunctionTransformer(convert_to_category)

    # Actualización del transformer categórico con el nuevo paso
    categorical_transformer = Pipeline(steps=[
        ('to_category', category_converter),
        ('imputer', SimpleImputer(strategy='most_frequent', missing_values=np.nan)),
        ('onehot', OneHotEncoder(drop='first', handle_unknown='ignore'))
    ])

    # Definición del preprocessor con el ColumnTransformer
    # Asumiendo que X_train ya está definido en alguna parte del código
    preprocessor = ColumnTransformer(transformers=[
        ("num", numeric_transformer, X_train.select_dtypes(exclude=['object', 'category']).columns),
        ("cat", categorical_transformer, X_train.select_dtypes(include=['object']).columns)
    ])

    mlflow.set_tracking_uri("http://10.43.101.156:8084")
    mlflow.set_experiment("model_tracking")

    # Parámetros para RandomizedSearchCV
    param_distributions = {
        'xgb__n_estimators': [100, 200, 300],
        'xgb__learning_rate': [0.01, 0.1, 0.2],
        'xgb__max_depth': [3, 5, 7],
        'xgb__subsample': [0.8, 0.9, 1.0]
    }

    # Configurar el preprocesador y el modelo en un pipeline
    clf = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("xgb", XGBClassifier(use_label_encoder=False, eval_metric='logloss'))
    ])

    # Entrenar el modelo con RandomizedSearchCV utilizando el conjunto de validación para evaluar
    search = RandomizedSearchCV(clf, param_distributions, n_iter=6, scoring='accuracy', cv=3, random_state=42)
    search.fit(X_train, y_train)  # Entrenar con el conjunto de entrenamiento

    # Mejor estimador después de la búsqueda
    best_clf = search.best_estimator_

    # Uso del conjunto de prueba para evaluar el modelo final
    y_pred = best_clf.predict(X_validation)
    score = best_clf.score(X_validation, y_validation)
    classification_rep = classification_report(y_validation, y_pred, output_dict=True)
    precision = classification_rep['weighted avg']['precision']
    recall = classification_rep['weighted avg']['recall']

    # Log en MLflow
    with mlflow.start_run(run_name="model_experiment") as run:
        mlflow.log_metric("accuracy", score)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.sklearn.log_model(best_clf, "model")
        model_uri = f"runs:/{run.info.run_id}/model"
        model_details = mlflow.register_model(model_uri=model_uri, name="model_experiment")

    # Determinar el mejor modelo
    client = mlflow.tracking.MlflowClient()
    filter_string = "name='model_experiment'"
    all_model_versions = client.search_model_versions(filter_string)
    best_model = None
    best_accuracy = 0

    for model in all_model_versions:
        model_run = client.get_run(model.run_id)
        model_accuracy = model_run.data.metrics['accuracy']
        if model_accuracy > best_accuracy:
            best_accuracy = model_accuracy
            best_model = model

    if best_model:
        client.transition_model_version_stage(
            name="model_experiment",
            version=best_model.version,
            stage="Production",
            archive_existing_versions=True
        )
        for model in all_model_versions:
            if model.version != best_model.version:
                client.transition_model_version_stage(
                    name="model_experiment",
                    version=model.version,
                    stage="Staging"
                )

    engine.dispose()
    engine_2.dispose()


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 5, 1),
}

dag = DAG('diabetes_batch_processing', default_args=default_args, schedule_interval='@hourly',concurrency=1)

# Tarea para obtener y almacenar los datos
t1 = PythonOperator(
    task_id='preprocessing_and_store',
    python_callable=fetch_and_store,
    dag=dag,
)

# Tarea para entrenar el modelo
t2 = PythonOperator(
    task_id='model_train',
    python_callable=model_train,
    dag=dag,
)

# Configuración de la dependencia
t1 >> t2
