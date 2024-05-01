# Entorno #

![Arquitectura.](./img/arquitectura.png) 

Inicialmente Airflow se encargará de ejecutar los DAGs para:

- Descargar los datos expuestos en la Data API y almacenarlos en la base de datos Mysql. Cabe indicar que la API encargada de entregar los datos se actualiza cada 5 minutos, por lo que el DAG de solucitud de datos tiene un retraso de 6 minutos para dar tiempo a la API a cambiar los datos aleatorios. Esto, en caso de que existan varias ejecuciones en la cola y así evitar que puedan ejecutarse simultaneamente, debido a que el DAG se ejecuta una vez al dia al tener el argumento catchup = True.
- Entrenar el modelo SVM con los datos extraidos,  registrar los experimentos con su respectiva metadata en mlflow y Mysql, y almacenar los modelos generados en minio. El entrenamiento del modelo cuenta con una etapa de random search de 5 iteraciones, por lo que la ejecución del mismo puede tomar varios minutos. 

Mlflow organiza el cliclo de vida de los modelos de machine learning mediante el registro de metadata producto del entrenamiento. La metadata incluye las métricas, versiones, expermientos y parámetros. Adicionalmente administra y crea los objetos de ejecución y configuración de los modelos creados.

Minio funciona como repositorio para los modelos y archivos de configuración. 

Para almacenar los datos descargados desde Airflow y metricas que se obtienen del entrenamiento de los modelos usamos el sistema de gestión Mysql, en el cual 2 bases de datos fueron configuradas:
- **mlflow**: Nombre de la base de datos de mlflow para almacenamiento de metadatos.
- **cover_type**: Nombre la base de datos que tiene el dataset solicitado a la api externa, para entrenar el modelo.

Por último se agregó una interfaz gráfica por medio de streamlit, para que el usuario ingrese al modelo y sus componentes(airflow, minio, mlflow, fastapi):

![Streamlit.](./img/streamlit.png) 

Streamlit se encuentra disponible en la url: 
http://10.43.101.156:8086/
# Configuración de Componentes #

Los siguientes servicios se despliegan a través del archivo ```docker-compose.yaml```.
## Airflow ##
Toda la configuración se encuentra definida en el archivo compose y se realizaron los siguientes cambios:

- En la sección **environment** se adicionaron las credenciales de minio, para establecer la conexión entre Airflow y el repositorio, y así poder almacenar los modelos entrenados dentro de los dags:
    ```
    MLFLOW_S3_ENDPOINT_URL: http://minio:9000
    AWS_ACCESS_KEY_ID: admin
    AWS_SECRET_ACCESS_KEY: supersecret
    ```
## Mlflow ##
Se creó un servicio en el docker compose de la siguiente manera:
```
mlflow_serv:
    build:
      context: .
      dockerfile: Dockerfile_mlflow
    ports:
      - "8084:5000" 
    command: >
      mlflow server
      --backend-store-uri mysql+pymysql://root:airflow@mysql:3306/mlflow
      --default-artifact-root s3://mlflows3
      --host 0.0.0.0
      --port 5000
      --serve-artifacts
    depends_on:
      - mysql
      - minio
    environment:
      MLFLOW_S3_ENDPOINT_URL: http://minio:9000
      AWS_ACCESS_KEY_ID: admin
      AWS_SECRET_ACCESS_KEY: supersecret
 ```
El servicio cuenta con su propio docker file(Dockerfile_mlfow), el cual instala las librerias necesarias para mlflow.

 Se habilitó el puerto 8084 para acceder a la interfaz, se estableció conexión para el almacenamiento del backend con Mysql y minio, y con esto almacenar los objetos en el bucket mlflows3.

## Minio ##
Configuración minio:
 ```
minio:
    container_name: Minio
    command: server /data --console-address ":9001"
    environment:
      - MINIO_ROOT_USER=admin
      - MINIO_ROOT_PASSWORD=supersecret
    image: quay.io/minio/minio:latest
    ports:
      - '9000:9000'
      - '8083:9001'
    volumes:
      - ./minio:/data
    restart: unless-stopped
 ```
Como podemos ver le asignamos unas credenciales para el acceso al servicio, el cual responde por dos puertos:
- 9000 para la consola
- 8083 para la interfaz gráfica
- Las credenciales para acceder al repositorio son: USUARIO: admin CONTRASEÑA: supersecret

## Fastapi ##
 ```
mi_api:
    build:
      context: .
      dockerfile: Dockerfile_api
    volumes:
      - ./app:/code/app
    ports:
      - "8085:8000"
    depends_on:
      - mlflow_serv
      - minio
    environment:
      MLFLOW_URI: "http://mlflow_serv:5000"
      MLFLOW_S3_ENDPOINT_URL: http://minio:9000
      AWS_ACCESS_KEY_ID: admin
      AWS_SECRET_ACCESS_KEY: supersecret
  ```
Para Fastapi creamos una imagen personalizada que responde por el puerto 8085. Adicionamos variables de entorno con datos de acceso para minio y mlflow. Para acceder a la documentación, se habilitó el puerto 8085.

Esta imagen también cuenta con su propio dockerfile(Dockerfile_api), que se encarga de ejecutar la aplicación ```main.py``` en uvicorn.

## Streamlit ##
```
streamlit_app:
    build:
      context: .
      dockerfile: Dockerfile_streamlit
    ports:
      - "8086:8501"
    depends_on:
      - mi_api
```
Este servicio también tiene una configuración adicional en el dockerfile **Dockerfile_streamlit** donde se ejecuta la aplicación ```app_streamlit.py```. El puerto utilizado para este servicio es el 8086.

# Ejecución #
Para levantar el servicio en el servidor debemos realizar los siguientes pasos:
- Digitamos ``` sudo su ``` para loguearnos como root.
- Ingresamos la clave.
- Desde la consola, vamos al directorio ``` /home/estudiante/mlopsG72024/proyecto2 ```
- Finalmente, estando en la carpeta proyecto2 ejecutamos ``` docker compose up ```.
- desde la URL http://10.43.101.156:8086/ se puede acceder a la interfaz de streamlit, la cual tiene links de acceso a las URLs de los demás servicios, a los cuales se pueden acceder por separado mediante http://10.43.101.156:XXXX, donde XXXX son los puertos habilitados para cada servicio que fueron mencionados previamente.


 
