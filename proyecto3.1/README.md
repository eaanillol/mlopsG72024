# Entorno #

![Arquitectura.](./img/arquitectura_3.png) 

Inicialmente Airflow se encargará de ejecutar los DAGs para:

- Descargar los datos de el servidor de las bases de datos ```Diabetes 130-US Hospitals for Years 1999-2008```, mediante la libreria ```ucimlrepo```. en donde se dividió el dataset en training, validation y test. Con la particularidad de que el dataset test se subió a la base de datos MySQL en batches de 15000.
```
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
```
Para lograr indicar a la función el ultimo indice cargado en la iteración anterior, se guardo este en una tabla adicional en la base de datos ***RAW_DATA***.

## Conexión con KUBERNETES

Para poder establecer conexion con KUBERNETES, con los servicios de MySQL y MINIO, se modificaron las URL de cada servicio dentro de docker-compose, de la siguiente forma: 
```
MLFLOW_S3_ENDPOINT_URL: http://10.43.101.156:31000
--backend-store-uri mysql+pymysql://root:airflow@10.43.101.156:30082/mlflow
```
Para poder establecer connexión con los puertos del nodo de kubernetes, se utiliza la URL de la maquina virtual ```10.43.101.156``` y se conecta al puerto establecido en para los servicios de MySQL y Minio, ```30082```  ```31000```, en el nodo de kubernetes, en el archivo -service.yaml de cada uno, como se definió en la variable nodePort.
```
  ports:
    - name: "9000"
      port: 9000
      nodePort: 31000
      targetPort: 9000
    - name: "8083"
      port: 8083
      targetPort: 9001
      nodePort: 31001
```
En donde el "nodePort" es el puerto habilitado para establecer conexiones externas al nodo.

## Observar la base de datos MySQL 

Puede observar las bases de datos mediante el servicio Adminer, en la url ```10.43.101.156:8081```, con las siguientes credenciales:
- Username: 10.43.101.156:30082
- password: airflow
  
## Configuración de la API

Dado que el servicio de FASTAPI fue habilitado dentro de Kubernetes, los cambios realizados en el archivo Main.py fueron los siguientes:
- Inicialmente la URL de MLFlow, al ser este un servicio externo a kubernetes, fue cambiada por ```MLFLOW_TRACKING_URI = "http://10.43.101.156:8084" ```, en donde la URL corresponde al puerto de salida de el servicio de MLFLOW configurado en Docker.
- Para conectarse a la base de datos de MySQL, se configuro con la URL correspondiente al puerto asignado en el servicio de kubernetes ```engine = create_engine('mysql+pymysql://root:airflow@10.43.101.156:30082/RAW_DATA')```

Adicionalmente, dentro de el archivo ***Main.py***, para que la API utilizara el modelo en producción para la inferencia, se definió la funcion load_model, con la siguiente particularidad. 

```
# Filtrar para encontrar la versión en producción
    production_versions = [mv for mv in model_versions if mv.current_stage == 'Production']
```
En donde se hace un barrido de las versiones del modelo disponible en airflow, y se selecciona aquel que este en stage de producción, que fue previamente asignado por medio de los DAGs de airflow, en base al siguiente criterio:

```
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
```

En donde se hace un barrido de todas las versiones del modelo disponibles, se comparan los accuracy de cada uno y, aquel que tenga mejor accuracy, es enviado a producción.

# Ejecución #
Para levantar el servicio en el servidor debemos realizar los siguientes pasos:
- Digitamos ``` sudo su ``` para loguearnos como root.
- Ingresamos la clave.
- Desde la consola, vamos al directorio ``` /home/estudiante/repository/mlopsG72024/proyecto3.1 ```
- Finalmente, estando en la carpeta proyecto2 ejecutamos ``` docker compose up ```.
- desde la URL http://10.43.101.156:8086/ se puede acceder a la interfaz de streamlit, la cual tiene links de acceso a las URLs de los demás servicios, a los cuales se pueden acceder por separado mediante http://10.43.101.156:XXXX, donde XXXX son los puertos habilitados para cada servicio que fueron mencionados previamente.


 
