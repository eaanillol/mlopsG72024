DVC:
Es un sistema de control de versiones de código abierto que complementa los sistemas de control de versiones tradicionales como Git al centrarse en la gestión de archivos grandes, conjuntos de datos, modelos y experimentos, que son comunes en los flujos de trabajo de aprendizaje automático.

Para cargar los datasets contenidos en el repositorio configurado en Google Drive, una vez haya clonado el repositorio y tenga acceso al folder "proyecto1", ejecute el siguiente comando: ```dvc pull```



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
