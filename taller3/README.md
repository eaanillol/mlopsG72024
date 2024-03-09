# Descargar Repositorio #
Nuestro repositorio es público, y lo podemos descargar ejecutando el siguiente comando:

  ```git clone  https://github.com/eaanillol/mlopsG72024.git```

# docker-compose.yaml #
Una serie de cambios fueron implementados en este archivo para lograr implementar los diferentes requerimientos del taller:

1. Para crear una instancia de una base de datos mysql, fue necesario incluir el servicio **mysql** dentro del compose:
```
 mysql:
    image: mysql:latest
    ports:
      - "3306:3306"
    environment:
      MYSQL_ROOT_PASSWORD: airflow  
      MYSQL_DATABASE: penguin_data
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 3
      start_period: 10s
    restart: always
```
