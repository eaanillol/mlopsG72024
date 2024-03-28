# Usamos la imagen de Airflow como base
FROM apache/airflow:2.6.0-python3.8

# Definir argumentos de entorno necesarios para MLflow
ARG MLFLOW_S3_ENDPOINT_URL=http://10.43.101.156:9000
ARG AWS_ACCESS_KEY_ID=admin
ARG AWS_SECRET_ACCESS_KEY=supersecret

# Establecer variables de entorno basadas en los argumentos
ENV MLFLOW_S3_ENDPOINT_URL=${MLFLOW_S3_ENDPOINT_URL}
ENV AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
ENV AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}

# Cambiar al usuario root temporalmente para crear el directorio de trabajo y ajustar permisos
USER root
RUN mkdir /work && chown airflow: /work
WORKDIR /work

# Copiar el archivo requirements.txt al contenedor
COPY requirements.txt /work/requirements.txt

# Cambiar de nuevo al usuario airflow antes de instalar las dependencias
USER airflow

# Instalar dependencias adicionales desde requirements.txt
# Asegúrate de que tu requirements.txt no incluya jupyter o jupyterlab si decides excluirlos
RUN pip install --user --no-cache-dir -r /work/requirements.txt

# Exponer puertos necesarios (ejemplo: el puerto web de Airflow y otros que necesites)
EXPOSE 8080 8081 8082

# Utilizar el ENTRYPOINT y CMD por defecto de Airflow