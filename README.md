Para traducir el comando de Docker en un Docker compose, se realizaron las siguientes acciones:

- El primer servicio se llama "jupiter-taller2:"
- **container_name:** reemplaza el comando "--name" que se utiliza para establecer un nombre específico   para la instancia del contenedor.
- **ports:** reemplaza "-p" el cual publica el puerto puerto_maquina_anfitriona:puerto_del_contenedor.
- **volumes:** reemplaza "-v" el cual monta el volumen de enlace como archivo o carpeta, en donde '.:/tfx/src' reemplaza las variables $PWD y /tfx/src
- **entrypoint:** reemplaza a "--entrypoint"
- **image:** variable que define la imagen "tensorflow/tfx:1.12.0:"

Existen algunos commandos como "it" y "rm" que no estan disponibles en docker compose. Para sustituirlos de realizaron las siguientes acciones:

- ****stdin_open:** true** 1/2 comandos que sustituyen el comando it que permite un modo interactivo.
- **tty: true:** 2/2 comandos que sustituyen el comando it que permite un modo interactivo.
  

