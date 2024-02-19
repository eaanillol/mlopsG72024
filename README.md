Para traducir el comando de Docker en un Docker compose, se realizaron las siguientes acciones:

  1. ****stdin_open:** true** 1/2 comandos que sustituyen el comando it que permite un modo interactivo.

Existen algunos commandos como "it" y "rm" que no estan disponibles en docker compose. Para sustituirlos de realizaron las siguientes acciones:

  2. **tty: true:** 2/2 comandos que sustituyen el comando it que permite un modo interactivo.
  3. **container_name:** reemplaza el comando "--name" que se utiliza para establecer un nombre específico   para la instancia del contenedor

