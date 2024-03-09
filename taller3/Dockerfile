FROM apache/airflow:2.6.0

# Usuarui
USER airflow

# Instalar dependencias adicionales desde requirements.txt
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt