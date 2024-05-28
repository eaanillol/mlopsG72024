# Entorno #

![Arquitectura.](./img/arquitectura_3.png) 

Inicialmente Airflow se encargará de ejecutar los DAGs para:

- Descargar los datos de el servidor de la API, teniendo en cuenta las siguiente peculiaridades.
    1. existe un numero limitado de peticiones. Una vez se alcanza el limite, la API retornara el siguiente mensaje: ```Ya se recolectó toda la información minima necesaria```
   2. Existe un metodo de reiniciar las peticiones y adquirir los datos desde el batch 1.
    ```
    if "detail" in data:
            if data["detail"] == "Ya se recolectó toda la información minima necesaria":
                parent_directory = 'http://10.43.101.149:80/restart_data_generation?group_number=7'
                response = requests.get(parent_directory)
                parent_directory = 'http://10.43.101.149:80/data?group_number=7'
                response = requests.get(parent_directory)
                clear_table(engine, "real_estate")
                clear_table(engine_2, "real_estate")     
                data = response.json()    
                print("datos",data)
    ```
Mediante este codigo, se hace una revision de los datos retornados por la API y, si se recolectó toda la infomacion necesaria, se realizan 2 solicitudes adicionales, la primera, para reiniciar el conteo y la segunda, para obtener el primer batch. Posteriormente se eliminan todos los datos de las tablas para almacenar el primer batch.

- Comparar los datos de el batch previo y el batch actual, para determinar si la diferencia entre los datos es significativa y vale la pena entrenar una nueva version del modelo.
```
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
```
Mediante esta función, se extraen diferentes metricas de el dataset previo y el actual (media, desv. estandar, cuartil 50 y 75) y, si la diferencia entre estas 2 tablas es mayor a 15% en cualquiera de estas variables, se entrena una nueva version del modelo. Se eligieron estas variables dado que, por ejemplo, si el la diferencia del cuartil 50% entre las dos tablas es significativa, esto indica que el valor medio de ambos grupos es diferente, por lo que la distribución de los datos cambió drasticamente. El registro de estas metricas y el resultado de las comparaciones queda almacenado en una tabla en MySQL.
- Realizar o no el entrenamiento del modelo en base a la variable **retrain** obtenida de la función ```compare_batch```.
# SHAP

Para interpretar el modelo, se implemento la libreria SHAP y el servicio de Jupyter notebook, en donde se pre-establecieron una serie de lineas de codigo para cargar el mas reciente modelo en producción y generar las diferentes graficas para interpretación.Comp tal, hubieron 2 versiones del modelo que entraron a fase de producción, la version 1 y 16, de las cuales se obtuvieron las siguientes metricas:

![Arquitectura.](./img/SHAP_M1-1.png) 
![Arquitectura.](./img/SHAP_M2-1.png) 

En la version 1, se observa que la variable que tenia mayor infuencia era la de baño, en donde, a mayor cantidad de baños, se observaba una mayor variación positiva del precio del inmueble. En la version 16, en donde habian mayor cantidad de datos para entrenar, se observó que la variable estado pasó a ser la de mayor importancia, seguida por la del tamaño del inmueble, como se muestra a continuación:

![Arquitectura.](./img/SHAP_M1-2.png)
![Arquitectura.](./img/SHAP_M2-2.png)

Las diferencias en los resultados de los dos modelos  (al observar los diagramas de descomposición de valores ) probablemente se deban al volumen de datos con que cada uno fue entrenado. Un modelo entrenado con más datos tiende a generalizar mejor y ser más robusto, lo que se refleja en cómo evalúa las características como el tamaño del lote y la ubicación. Esto puede hacer que uno de los modelos sea más sensible a ciertas características debido a una mayor exposición a variaciones en los datos. Por otro lado, el entrenamiento con un conjunto de datos más limitado podría llevar a un modelo a sobrevalorar ciertas características que aparecen con más frecuencia en ese conjunto específico, afectando la precisión de sus predicciones.

![Arquitectura.](./img/SHAP_M1-3.png)
![Arquitectura.](./img/SHAP_M2-3.png)
 
# Configuración de la API

Dentro de el archivo ***Main.py***, para que la API utilizara el modelo en producción para la inferencia, se definió la funcion load_model, con la siguiente particularidad. 

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
Finalmente, para guardar todos los datos ingresados por usuario en cada inferencia, se creó la tabla **new_real_state** en la base de datos RAW data.
```
engine = create_engine('mysql+pymysql://root:airflow@10.43.101.156:8082/RAW_DATA')
   
    try:
        model, version = load_model()
        columns = [" brokered_by", "status", "price", "bed", "bath", "acre_lot", 
		   "street", "city", "state", "zip_code", "house_size", "prev_sold_date"]

        # Convertir la entrada a dataframe de pandas, guardar datos en MySQL y limpiar los datos
        input_df = pd.DataFrame([input.dict()],columns = columns)
        input_df.to_sql('new_real_estate', con=engine, if_exists='append', index=False)
```

# Github Actions y Docker Hub
Github Actions es una herramienta proporcionada por Github para realizar despliegues continuos y/o ejecución de acciones que evaluan los archivos o códigos subidos a un repositorio.

## Configuración
Para usar Github Actions con Docker debemos crear credenciales en Docker Hub que  se usaran en la configuración inicial del Actions.

### Docker
- Ingresamos a la página de Docker Hub https://hub.docker.com/
- Ahora logueése con su usuario de Github y vaya a **My Account**
![Cuenta Dockerhub](./img/dockerhub_account_1.png)
- Abra la opción de **Security** y luego click en **New Access Token**
![Cuenta Dockerhub](./img/dockerhub_account_2.png)
- Le damos un nombre al token de acceso con los permisos necesarios y finalmente damos click a **Generar**.
- Copie las credenciasles creadas en un lugar seguro, ya que vamos a usarlas en Github Actions para poder hacer push a las imágenes Docker.

### Github Actions
Primero debemos abrir el repositorio https://github.com/eaanillol/mlopsG72024 y nos movemos  a la rama **proyecto-final**. Vamos al tab de settings en el repositorio:
![Settings Guithub Actions](./img/githubactions_1.png)

Bajamos hasta la sección de security y entramos a la opción **Actions**:
![Settings Guithub Actions](./img/githubactions_2.png)

Como vamos a agregar las variables de usuario y contraseña damos click en **New repository secret** para crearlas.

Ya teniendo las variables creadas, debemos agregar un archivo YML en la ruta *.github/workflows/github-actions-demo.yml*. El contenido del archivo s e puede ver en: https://github.com/eaanillol/mlopsG72024/blob/proyecto-final/.github/workflows/github-actions-demo.yml

Ahora vamos a explicar las partes más importantes del archivo. Al principio se define cuando se ejecuta Github Actions:
```
on: 
  push:
    branches:
      - proyecto-final
```
Aquí le estamos diciendo al workflow que se ejecute cada vez que se haga un *push*  a la rama  *proyecto-final*. Luego definimos las propiedades del job junto con los pasos a ejecutar.

```
jobs:
  Explore-GitHub-Actions:
    runs-on: ubuntu-latest
```
*runs-on* le dice al job en que sistema operativo se debe ejecutar.

Luego definimos los pasos. Al iniciar el deployment nos logueamos en Docker Hub con las credenciales creadas:

``` 
    steps:
      #Pasos de información
      #Pasos de información
      #Deployment
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_PASSWORD }}
``` 
Paso siguiente es decirle a Github como crear las imágenes para hacer push en Docker Hub. En el archivo YML le pasamos la lista de archivos para los builds de cada imagen:

``` 
      - name: Build and push API MLOPs
        uses: docker/build-push-action@v5
        with:
          push: true
          file: ./proyectoFinal/Dockerfile_api
          tags: ${{ secrets.DOCKERHUB_TAG }}/proyectofinal-mi_api:latest
      - name: Build and push Streamlit MLOPs
        uses: docker/build-push-action@v5
        with:
          push: true
          file: ./proyectoFinal/Dockerfile_streamlit
          tags: ${{ secrets.DOCKERHUB_TAG }}/proyectofinal-streamlit_app:latest
      - name: Build and push Jupyter MLOPs
        uses: docker/build-push-action@v5
        with:
          push: true
          file: ./proyectoFinal/Dockerfile_jupyter
          tags: ${{ secrets.DOCKERHUB_TAG }}/proyectofinal-jupyter:latest
      - name: Build and push MLFLOW MLOPs
        uses: docker/build-push-action@v5
        with:
          push: true
          file: ./proyectoFinal/Dockerfile_mlflow
          tags: ${{ secrets.DOCKERHUB_TAG }}/proyectofinal-mlflow_serv:latest
      - name: Build and push Airflow MLOPs
        uses: docker/build-push-action@v5
        with:
          push: true
          file: ./proyectoFinal/Dockerfile
          tags: ${{ secrets.DOCKERHUB_TAG }}/proyectofinal-airflow:latest
```
Probamos el workflow haciendo un push a la rama **proyecto-final**. Abrimos la pestaña de de Actions y revisamos la ejecución actual para revisar el proceso:
![Actions Guithub Actions](./img/githubactions_3.png)

# Ejecución de la Arquitectura
A continuación mostraremos el paso a paso para la ejecución  del proyecto.

## Docker Compose
Para levantar el servicio en el servidor debemos realizar los siguientes pasos:
- Digitamos ``` sudo su ``` para loguearnos como root.
- Ingresamos la clave.
- Desde la consola, vamos al directorio ``` /home/estudiante/repository/mlopsG72024/proyectoFinal ```
- Finalmente, estando en la carpeta proyecto2 ejecutamos ``` docker compose up ```.
- desde la URL http://10.43.101.156:8086/ se puede acceder a la interfaz de streamlit, la cual tiene links de acceso a las URLs de los demás servicios, a los cuales se pueden acceder por separado mediante http://10.43.101.156:XXXX, donde XXXX son los puertos habilitados para cada servicio que fueron mencionados previamente.


 
