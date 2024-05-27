import time
import mlflow
import requests
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
from sklearn.pipeline import Pipeline
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import mean_squared_error, r2_score
from xgboost import XGBRegressor
from scipy.stats import randint, uniform

engine = create_engine('mysql+pymysql://root:airflow@10.43.101.156:8082/RAW_DATA')
engine_2 = create_engine('mysql+pymysql://root:airflow@10.43.101.156:8082/CLEAN_DATA')

def clean_data(data):
    # Eliminación de variables categoricos con muchas clases y la fecha, que no aporta al modelo
    data.drop([" brokered_by", "street","zip_code", "city","status", "prev_sold_date"],axis=1,inplace=True)
    data["state"] = data["state"].astype('category')
    price_data = data['price']
    # Filtrar el DataFrame para excluir los valores en el rango de 0 a 1000
    data = data[~((price_data >= 0) & (price_data <= 1000))]
    return data

def compare_batch(prev_data,new_data):
    stats_prev = prev_data.describe().drop(["zip_code","street"],axis=1)
    stats_combined = new_data.describe().drop(["zip_code","street"],axis=1)
    decision = False
    # Umbrales de cambio aceptables para cada estadística
    thresholds = {
        'mean': 0.15,  # 15% de cambio
        'std': 0.15,   # 15% de cambio
        '50%': 0.15,  # 15% de cambio
        '75%': 0.15   # 15% de cambio
                }
    columns = []
    values = []
    for stat in ['mean', 'std', '50%', '75%']:
        change = abs((stats_combined.loc[stat] - stats_prev.loc[stat]) / stats_prev.loc[stat])
        for i in range(0,len(change)):
            title = stat.replace("%","")
            columns.append(change.index[i]+"_" + title)
            values.append(change[i])
        if any(change > thresholds[stat]):
            decision = True
    stat_df = pd.DataFrame([values], columns = columns)
    stat_df["retrain"] = decision
    return stat_df

def manage_data(engine, new_batch):
    # Conectar con la base de datos y crear la tabla si no existe
    with engine.connect() as conn:
        # Crear la tabla con las especificaciones dadas
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS real_estate (
                id INT AUTO_INCREMENT PRIMARY KEY,
                brokered_by VARCHAR(255),
                status VARCHAR(255),
                price FLOAT,
                bed FLOAT,
                bath FLOAT,
                acre_lot FLOAT,
                street FLOAT,
                city VARCHAR(255),
                state VARCHAR(255),
                zip_code FLOAT,
                house_size FLOAT,
                prev_sold_date VARCHAR(255)
            );
        """))
        # Crear tabla para almacenar resultados de comparaciones si no existe
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS data_comp (
                id INT AUTO_INCREMENT PRIMARY KEY,
                price_mean FLOAT,
                bed_mean FLOAT,
                bath_mean FLOAT,
                acre_lot_mean FLOAT,
                house_size_mean FLOAT,
                price_std FLOAT,
                bed_std FLOAT,
                bath_std FLOAT,
                acre_lot_std FLOAT,
                house_size_std FLOAT,	
                price_50 FLOAT,
    	        bed_50 FLOAT,
    	        bath_50 FLOAT,
    	        acre_lot_50 FLOAT,
    	        house_size_50 FLOAT,
    	        price_75 FLOAT,
    	        bed_75 FLOAT,
 	        bath_75 FLOAT,
	        acre_lot_75 FLOAT,
    	        house_size_75 FLOAT,
	        retrain BOOLEAN
            );
        """))
        # Verificar el estado de los datos
        existing_data = pd.read_sql("SELECT * FROM real_estate", conn)
        if existing_data.empty:
            # Insertar el primer batch de datos si la tabla está vacía
            new_batch.to_sql('real_estate', con=conn, index=False, if_exists='replace')
            print("Primera carga de datos realizada.")
        else:
            # Combina el nuevo batch con los datos existentes
            combined_data = pd.concat([existing_data, new_batch]).reset_index(drop=True)
            combined_data.drop_duplicates(inplace=True)      
            # Comparar el dataset nuevo con el anterior usando una función definida
            comparison_result = compare_batch(existing_data, combined_data)
            print(comparison_result)
            # Insertar los resultados de la comparación en la tabla data_comp
            comparison_result.to_sql('data_comp', con=conn, index=False, if_exists='append')

            # Guardar el nuevo dataset si es necesario
            if comparison_result['retrain'][0]:
                combined_data.to_sql('real_estate', con=conn, index=False, if_exists='replace')
                print("Nuevo batch añadido y decisiones tomadas.")
            else:
                print("No se requiere acción adicional.")

# Crear una función para limpiar la tabla
def clear_table(engine, table_name):
    with engine.connect() as connection:
        # Usar una transacción para asegurar que la operación sea atómica
        with connection.begin() as transaction:
            try:
                # Ejecutar la sentencia SQL para eliminar todos los datos de la tabla
                connection.execute(text(f"DELETE FROM {table_name};"))
                # Confirmar la transacción si todo sale bien
                transaction.commit()
                print(f"Todos los datos han sido eliminados de la tabla {table_name}.")
            except Exception as e:
                # En caso de error, revertir la transacción
                transaction.rollback()
                print(f"Error al limpiar la tabla {table_name}: {e}")

def fetch_and_store(): 
    # Cargar los datos
    parent_directory = 'http://10.43.101.149:80/data?group_number=7'
    #Realiza la solicitud GET a la API
    response = requests.get(parent_directory)
    data = response.json()
    # Definir los nombres de las columnas
    column_names = [
                " brokered_by", "status", "price", "bed", "bath", "acre_lot", "street", 
                "city", "state", "zip_code", "house_size","prev_sold_date"
    ]
    if "detail" in data:
        if data["detail"] == "Ya se recolectó toda la información minima necesaria":
            parent_directory = 'http://10.43.101.149:80/restart_data_generation?group_number=7'
            #Realiza la solicitud GET a la API 2 veces, una para reiniciar el batch y la otra para extraer el primer batch
            response = requests.get(parent_directory)
            parent_directory = 'http://10.43.101.149:80/data?group_number=7'
            response = requests.get(parent_directory)
            clear_table(engine, "real_estate")
            clear_table(engine_2, "real_estate")     
            data = response.json()    
            print("datos",data)

    house_price = pd.DataFrame(data["data"],columns = column_names)

    manage_data(engine, house_price)

    query = "SELECT * FROM real_estate"
    # Leer los datos desde MySQL
    house_price = pd.read_sql(query, con=engine)
    #limpiar los datos
    house_price_clean =clean_data(house_price.copy())
    house_price_clean.to_sql('real_estate', con=engine_2, if_exists='replace', index=False)
    # Separar las características y el objetivo
    X = house_price.drop('price', axis=1)
    y = house_price['price']
    # Separar las características y el objetivo
    X_c = house_price_clean.drop('price', axis=1)
    y_c = house_price_clean['price']
    #train-test-validation
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.25, random_state=42)
    X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X_c, y_c, test_size=0.2, random_state=42)
    X_train_c, X_val_c, y_train_c, y_val_c = train_test_split(X_train_c, y_train_c, test_size=0.25, random_state=42)
    #train data
    clean_train_data = pd.concat([X_train_c, y_train_c], axis=1)
    clean_train_data.to_sql('real_estate', con=engine_2, if_exists='replace', index=False)
    # Combina las características y los targets en un solo DataFrame para validación
    val_data = pd.concat([X_val, y_val], axis=1)
    clean_val_data = pd.concat([X_val_c, y_val_c], axis=1)
    # Combina las características y los targets en un solo DataFrame para pruebas
    test_data = pd.concat([X_test,y_test], axis=1)
    clean_test_data = pd.concat([X_test_c,y_test_c], axis=1)
    # Almacenar los conjuntos de validación y test
    val_data.to_sql('real_estate_val', con=engine, if_exists='replace', index=False)
    test_data.to_sql('real_estate_test', con=engine, if_exists='replace', index=False)
    clean_val_data.to_sql('real_estate_val', con=engine_2, if_exists='replace', index=False)
    clean_test_data.to_sql('real_estate_test', con=engine_2, if_exists='replace', index=False)

def model_train():
    # Crear una consulta SQL como un objeto de texto para ser ejecutado.
    query_A = text("SELECT * FROM real_estate")
    query_B = text("SELECT * FROM real_estate_val")
    query_C = text("SELECT * FROM real_estate_test")
    retrain_d = text("SELECT * FROM data_comp")
    # Ejecuta la consulta y carga los datos en un DataFrame de pandas
    retrain = pd.read_sql(retrain_d,engine.connect())

    if retrain['retrain'].iloc[-1] == False:
        print("model will not be trained")
    else:
        # Ejecuta la consulta y carga los datos en un DataFrame de pandas
        train_data = pd.read_sql(query_A, engine_2.connect())
        validation_data = pd.read_sql(query_B, engine_2.connect())
        test_data = pd.read_sql(query_C, engine_2.connect())
        # Separar características y etiquetas para el conjunto de entrenamiento
        X_train = train_data.drop('price', axis=1)
        y_train = train_data['price']
        # Separar características y etiquetas para el conjunto de prueba
        X_test = test_data.drop('price', axis=1)
        y_test = test_data['price']
        # Separar características y etiquetas para el conjunto de validación
        X_validation = validation_data.drop('price', axis=1)
        y_validation = validation_data['price']
        
        # Definir el transformador para variables numéricas
        numeric_features = ['bed', 'bath', 'acre_lot', 'house_size']
        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='mean')),  # Imputa valores faltantes con la media
            ('scaler', StandardScaler())                 # Escala los datos
        ])

        # Definir el transformador city variables categóricas
        categorical_features = ['state']
        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),  # Imputa valores faltantes con la moda
            ('onehot', OneHotEncoder(handle_unknown='ignore'))     # Codificación one-hot
        ])

        # Crear el preprocesador usando ColumnTransformer
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('cat', categorical_transformer, categorical_features)
            ])
        
        # Configurar MLflow
        mlflow.set_tracking_uri("http://10.43.101.156:8084")
        mlflow.set_experiment("model_tracking")

        # Crear el pipeline completo
        xgb_pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('xgb', XGBRegressor(objective='reg:squarederror', n_jobs=-1))
        ])

        # Definir el espacio de búsqueda de hiperparámetros
        param_dist = {
            'xgb__n_estimators': randint(50, 200),
            'xgb__max_depth': randint(3, 10),
            'xgb__learning_rate': uniform(0.01, 0.3),
            'xgb__subsample': uniform(0.7, 0.3),
            'xgb__colsample_bytree': uniform(0.7, 0.3)
        }

        # Configurar RandomizedSearchCV
        random_search = RandomizedSearchCV(xgb_pipeline, param_distributions=param_dist, n_iter=10, cv=3, n_jobs=-1, random_state=42)

        # Ajustar el modelo
        random_search.fit(X_train, y_train)

        # Mejor modelo después de la búsqueda
        best_model = random_search.best_estimator_

        # Uso del conjunto de prueba para evaluar el modelo final
        y_pred = best_model.predict(X_validation)
        rmse = np.sqrt(mean_squared_error(y_validation, y_pred))
        r2 = r2_score(y_validation, y_pred)

        # Log en MLflow
        with mlflow.start_run(run_name="model_experiment") as run:
            mlflow.log_metric("RMSE", rmse)
            mlflow.log_metric("R2", r2)
            mlflow.sklearn.log_model(best_model, "model")
            model_uri = f"runs:/{run.info.run_id}/model"
            model_details = mlflow.register_model(model_uri=model_uri, name="model_experiment")

        # Determinar y manejar el mejor modelo
        client = mlflow.tracking.MlflowClient()
        filter_string = "name='model_experiment'"
        all_model_versions = client.search_model_versions(filter_string)
        best_model = None
        best_rmse = float('inf')

        for model in all_model_versions:
            model_run = client.get_run(model.run_id)
            model_rmse = model_run.data.metrics['RMSE']
            if model_rmse < best_rmse:
                best_rmse = model_rmse
                best_model = model

        if best_model:
            client.transition_model_version_stage(
                name="model_experiment",
                version=best_model.version,
                stage="Production",
                archive_existing_versions=True
            )

    # Limpieza final si se usan conexiones de motor (opcional)
    engine.dispose()
    engine_2.dispose()

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 5, 22),
}

dag = DAG('real_state', default_args=default_args, schedule_interval='@daily',concurrency=1)

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
