DVC:
Es un sistema de control de versiones de código abierto que complementa los sistemas de control de versiones tradicionales como Git al centrarse en la gestión de archivos grandes, conjuntos de datos, modelos y experimentos, que son comunes en los flujos de trabajo de aprendizaje automático.

Para cargar los datasets contenidos en el repositorio configurado en Google Drive, una vez haya clonado el repositorio y tenga acceso al folder "proyecto1", ejecute el siguiente comando: ```dvc pull```. Este comando examina el archivo covertype.dvc contenido en la carpeta "data", el cual apunta a la ubicacion remota de los datasets y su hash, que se utiliza para determinar la version de los datos que deben ser cargadas en el folder. Para cargar los datos crea un sub-foder "covertype" en donde se almacenará la version de estos. **Nota:** al hacer pull por primera vez, es probable que necesite ingresar sus credenciales de google para acceder a la carpeta, la cual esta abierta a todo publico. La url de la carpeta en drive esta almacenada en el archivo config, en la carpeta ".dvc".

Una vez haya terminado de trabajar en el ambiente de trabajo de Docker, y los cambios aplicados a los datasets se hayan actualizado en la carpeta "covertype", debe almacenar la nueva version de los datos mediante el siguiente comando ```dvc add data/covertype```. Posteriormente actualice el archivo coverype.dvc mediante el comando ```git add data/covertype.dvc```, el cual almacenará el nuevo hash correspondiente a la nueva version de los datasets. Después de realizar estos pasos, también se puede ejecutar ```dvc push``` para sincronizar los cambios en los metadatos de DVC con el almacenamiento remoto (Google Drive).

**IMPORTANTE:** Una vez actualice el archivo covertype.dvc, es recomendable incluir un commit con información detallada de los cambios en el dataset ```git commit -m <detalles>``` (e.j. creación de nueva variable test1). Esto será necesario si desea cargar una version anterior del dataset.

En caso de que desee cargar una version previa de los datos, utilice los siguiente comandos: ```git log -- data/covertype.dvc``` el cual le mostrará una lista de las versiones previas del archivo covertype.dvc almacenadas en github con su respectivo commit. Identifique la version de covertype que desee recuperar e ingrese el siguiente comando  ```git checkout <commit tag> -- data/covertype.dvc```. Posteriormente, ejecute el comando ```dvc checkout -f data/covertype.dvc``` o ```dvc pull``` y DVC cargará la version de los datasets correspondiente al hash almacenado en la version del archivo covertype.dvc seleccionada. Las diferentes versiones de los datos estan almacenadas en la carpeta cache dentro del folder .dvc. Estas versiones previas solo se almacenan a nivel local.

Una vez finalice sus tareas y tenga una version final del dataset, ingrese de nuevo los comandos ```dvc add data/covertype```, ```git add data/covertype.dvc``` y ```dvc push``` para almacenar la ultima version de el dataset en el repositorio.


Para traducir el comando de Docker en un Docker compose, se realizaron las siguientes acciones:

- El primer servicio se llama "jupiter-taller2"
- **container_name:** reemplaza el comando "--name" que se utiliza para establecer un nombre específico   para la instancia del contenedor.
- **ports:** reemplaza "-p" el cual publica el puerto puerto_maquina_anfitriona:puerto_del_contenedor.
- **volumes:** reemplaza "-v" el cual monta el volumen de enlace como archivo o carpeta, en donde '.:/tfx/src' reemplaza las variables $PWD y /tfx/src
- **entrypoint:** reemplaza a "--entrypoint"
- **image:** variable que llama a la imagen "tensorflow/tfx:1.12.0:"

Existen algunos commandos como "it" que para sustituirlos se usaron dos atributos:

- ****stdin_open:** true** Comando que sustituyen el comando i que permite un modo interactivo. 
- **tty: true:** Comando que sustituyen el comando t que permite un modo interactivo.

**Nota:** la variable context: no es requerida al no necesitar subir el dockerfile para trabajar con jupyter. Lo que hacemos es cargar la imagen "tensorflow/tfx:1.12.0" para el docker.

En el archivo compose no hay una etiqueta para implementar la opción de comando --rm, y también tuvimos que dejar --name en el comando final con composer, por que la etiqueta container_name tiene un bug conocido. La información acerca de este problema está disponible [aquí](https://github.com/docker/compose/issues/2061)

Nuestro repositorio es público, y lop podemos descargar ejecutando el siguiente comando:
  ```git clone  https://github.com/eaanillol/mlopsG72024.git```

Luego abrimos la consola y nos ubicamos en la carpeta donde se descargó el repositorio. Luego desde la consola vamos a la carpeta taller 2 y ejecutamos el siguiente comando con compose:
- Windows: docker-compose -f .\docker-compose.yaml run --name tfx  --service-ports --rm jupiter-taller2
