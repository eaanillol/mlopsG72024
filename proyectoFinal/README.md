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
Mediante esta función, se extraer diferentes metricas de el dataset previo y el actual (media, desv. estandar, cuartil 50 y 75) y, si la diferencia entre estas 2 tablas es mayor a 15% en cualquiera de estas variables, se entrena una nueva version del modelo. Se eligieron estas variables dado que, por ejemplo, si el la diferencia del cuartil 50% entre las dos tablas es significativa, esto indica que el valor medio de ambos grupos es diferente, por lo que la distribución de los datos cambió drasticamente. El registro de estas metricas y el resultado de las comparaciones queda almacenado en una tabla en MySQL.
- Realizar o no el entrenamiento del modelo en base a la variable **retrain** obtenida de la función ```compare_batch```.
##GITHUB Actions
 
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
# Ejecución de la Arquitectura
A continuación mostraremos el paso a paso para la ejecución y montaje de la infraestructura del proyecto.



## Kubernetes
Para Kubernetes usamos la implementación de Microk8s que nos permitió levantar cada uno de los nodos y pods necesarios. 

Para desplegar Kubernetes primero debemos asegurarnos que el servicio de Microk8s esté funcionando:
```sudo microk8s status ```

![Arquitectura.](./img/microk8s_status.png) 

Como podemos ver el servicio está corriendo correctamente. En caso tal, el servicio se encuentre apagado ejecutamos:
```sudo microk8s start ```

Luego vamos a la ruta donde tenemos todos los archivos del proyecto 3:

``` cd /home/estudiante/repository/mlopsG72024/proyecto3.1 ```

Para facilitar el uso de algunos comandos usados frecuentemente, se crearon algunos shell files como:
- ```  start-microk8s-dashboard.sh ```: Inicia el dashboard de Kubernetes en el puerto 8089 o cualquier otro puerto que se le indique.
- ``` get-current-token-microk8s.sh ```: Obtiene el token de acceso para el dashboard.

Ahora procedemos a ejecutar el comando para ver el dashboard desde fuera de la máquina virtual:
```sudo sh  start-microk8s-dashboard.sh ```

![Arquitectura.](./img/microk8s_start_dashboard.png) 

Ingresando por https a la URL https://10.43.101.156:8089:

![Arquitectura.](./img/kubernetes_login.png) 

Para obtener el token de acceso ejecutamos ```sudo sh  get-current-token-microk8s.sh ```. Por consiguiente, copiamos y pegamos el valor obtenido para loguearnos a la página de Kubernetes:

![Arquitectura.](./img/kubernetes_dashboard.png) 

Como podemos ver, tenemos el nodo con los pods corriendo correctamente.

## Docker Compose
Para levantar el servicio en el servidor debemos realizar los siguientes pasos:
- Digitamos ``` sudo su ``` para loguearnos como root.
- Ingresamos la clave.
- Desde la consola, vamos al directorio ``` /home/estudiante/repository/mlopsG72024/proyecto3.1 ```
- Finalmente, estando en la carpeta proyecto2 ejecutamos ``` docker compose up ```.
- desde la URL http://10.43.101.156:8086/ se puede acceder a la interfaz de streamlit, la cual tiene links de acceso a las URLs de los demás servicios, a los cuales se pueden acceder por separado mediante http://10.43.101.156:XXXX, donde XXXX son los puertos habilitados para cada servicio que fueron mencionados previamente.


 
