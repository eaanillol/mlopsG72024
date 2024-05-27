# Dockerfile
FROM python:3.9.12

WORKDIR /code

COPY ./test_images/requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./test_images/*.py /code

# El comando para ejecutar la aplicación con Uvicorn. Ajusta la ruta del módulo si es necesario.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]