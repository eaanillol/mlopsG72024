#!bin/bash

echo "Preparing directories and IDD for Airflow"
mkdir -p  dags scripts notebooks logs plugins datos
echo  "AIRFLOW_UID=$(id -u)" > .env
sleep 1
echo "FINISHED"

