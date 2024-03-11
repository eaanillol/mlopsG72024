# Descargar Repositorio #
Nuestro repositorio es público, y lo podemos descargar ejecutando el siguiente comando:

  ```git clone  https://github.com/eaanillol/mlopsG72024.git```

# docker-compose.yaml #
Una serie de cambios fueron aplicados en este archivo para lograr implementar los diferentes requerimientos del taller:

1. Para crear una instancia de una base de datos mysql, fue necesario incluir el servicio **mysql** dentro del docker-compose y el volume **mysql_data**:
```
mysql:
    # Nombre del servicio
    image: mysql:latest  # Imagen Docker para el contenedor MySQL
    ports:
      - "3306:3306"  # Mapeo de puertos del contenedor al host
    environment:
      MYSQL_ROOT_PASSWORD: airflow  # Contraseña de root para MySQL
      MYSQL_DATABASE: penguin_data  # Nombre de la base de datos MySQL
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]  # Comando de verificación de salud
      interval: 10s  # Frecuencia de la verificación de salud
      timeout: 5s  # Tiempo máximo de espera para la verificación de salud
      retries: 3  # Número de intentos de verificación de salud
      start_period: 10s  # Tiempo antes de iniciar las verificaciones de salud
    restart: always  # Política de reinicio del contenedor
```

2. Para cargar la tabla **penguins_lter.csv** y subirla a la base de datos, es necesario incluir este dataset en ```_PIP_ADDITIONAL_REQUIREMENTS``` para que quede almacenado en el contenedor.
   
```
- ${AIRFLOW_PROJ_DIR:-.}/datos:/opt/airflow/datos
```

3. Para poder manipular el archivo penguins_lter como un dataframe y conseguir entrenar un modelo de machine learning, es necesario cargar las librerias requeridas dentro de el contenedor, es decir, es requerido extender la imagen e incluir los paquetes necesarios para crear y entrenar el modelo. Para ello, se comenta la linea ``` image: ${AIRFLOW_IMAGE_NAME:-apache/airflow:2.6.0} ```, y se habilita la linea ```build: .```, la cual lee el archivo Dockerfile que contiene la lista de librerias (guardadas en el archivo **requirements.txt**) y la imagen de airflow necesaria para el contenedor:

```
FROM apache/airflow:2.6.0

# Usuarui
USER airflow

# Instalar dependencias adicionales desde requirements.txt
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt
```
4. una vez realizados los cambios, simplemente ejecutando ```docker-compose up``` despues del build, todos los contenedores para los servicios incluidos en airflow deberían ser ejecutados. apauede corroborar que sea asi con el comando ```docker ps```

# Ejecución de DAGS

- Primero debemos ejecutar el DAG **data_loading_dag** que se encargará de copiar los datos desde el excel. 
- Luego pasamos a correr el DAG **svm_training_dag** para preprocesar y entrenar el modelo del cual esperamos obtener un archivo joblib llamado **SVM_model.joblib**. Dicho archivo quedará guardado en la carpeta compartida de **datos**.
- Finalmente procedemos a eliminación de los datos con el DAG **delete_data_dag**