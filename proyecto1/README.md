# Descargar Repositorio #
Nuestro repositorio es público, y lo podemos descargar ejecutando el siguiente comando:

  ```git clone  https://github.com/eaanillol/mlopsG72024.git```

  Abrimos la consola y nos ubicamos en la carpeta donde se descargó el repositorio. Luego desde la consola vamos a la carpeta **project1** y como primera medida procedemos a instalar  DVC:
  
  ```pip install dvc```

Después instalamos la librería dvc_gdrive:

  ```pip install dvc_gdrive```

Finalmente ejecutamos el siguiente comando con compose:
- Windows: ```docker-compose -f .\docker-compose.yaml run --name tfx  --service-ports --rm jupiter-project1```

**Importante**: Al ejecutar el proyecto en windows recomendamos bajar el repositorio en una carpeta de la raíz C:. Esto con el fin de evitar el error de directorio "filename too large"

# DVC #
Es un sistema de control de versiones de código abierto que complementa los sistemas de control de versiones tradicionales como Git al centrarse en la gestión de archivos grandes, conjuntos de datos, modelos y experimentos, que son comunes en los flujos de trabajo de aprendizaje automático.

Para cargar los datasets contenidos en el repositorio configurado en Google Drive, una vez haya clonado el repositorio y tenga acceso al folder "proyecto1", ejecute el siguiente comando: 

```dvc pull``` 

Este comando examina los archivos **covertype.dvc** y **serving.dvc** contenidos en la carpeta **"data"**, los cuales apuntan a la ubicacion remota de los datasets. Los hash almacenados en dichos ficheros determinan la version de los datos que deben ser usados en el folder. Para cargar los datos, automaticamente se crean los sub-foders **"covertype"** y **serving** en donde se almacenan los datasets con su última versión. **Nota:** al hacer pull por primera vez, es probable que necesite ingresar sus credenciales de google para acceder a la carpeta, la cual esta abierta a todo publico. La URL de la carpeta en drive esta almacenada en el archivo config, en la carpeta ".dvc".

Una vez realizado el pull en con dvc, se debe ejecutar las instrucciones en el ambiente de trabajo de Docker(jupyter). Los cambios aplicados a los datasets se actualizarán en la carpeta **"data"**. Luego almacenamos la nueva version de los datos mediante el siguiente comando: 

```dvc add data/covertype```

```dvc add data/serving```

 Posteriormente actualice los archivos **covertype.dvc** y **serving.dvc**  mediante el comando: 
 
 ```git add data/covertype.dvc```

  ```git add data/serving.dvc```
 
  El cual almacenará el nuevo hash correspondiente a la nueva version de los datasets. Después de realizar estos pasos, también se puede ejecutar ```dvc push``` para sincronizar los cambios en los metadatos de DVC con el almacenamiento remoto (Google Drive).

**IMPORTANTE:** Una vez actualice los archivos **covertype.dvc** y **serving.dvc**, es recomendable incluir un commit con información detallada de los cambios en el dataset:

```git commit -m "Mensajes de mis cambios"``` 

Esto será necesario si desea cargar una version anterior del dataset.

En caso de que desee cargar una version previa de los datos, utilice los siguiente comandos: 

```git log -- data/covertype.dvc``` 

```git log -- data/serving.dvc``` 

El cual le mostrará una lista de las versiones previas de los archivos dvc almacenados en github con su respectivo commit. Identifique la version de covertype que desee recuperar e ingrese el siguiente comando  ```git checkout <commit tag> -- data/covertype.dvc```. Posteriormente, ejecutamos los siguientes comandos para cargar uno a uno los datasets correspondientes a cada data:

 ```dvc checkout -f data/covertype.dvc```

 ```dvc checkout -f data/serving.dvc```

 O podemos hacer un pull con dvc y se actualizarán todos los dataset de nuestro repositorio dvc:
 
  ```dvc pull```
 
 Con esto, DVC cargará la version de los datasets correspondiente al hash almacenado en la version de los archivos dvc que tenemos. Las diferentes versiones de los datos estan almacenadas en la carpeta cache dentro del folder .dvc. Estas versiones previas solo se almacenan a nivel local.

Una vez finalice sus tareas y tenga una version final del dataset, ingrese de nuevo los comandos 

```dvc add data/covertype data/serving ```

```git add data/covertype.dvc data/serving.dvc```

 ```dvc push``` 
 
 para almacenar la ultima version de el dataset en el repositorio.




