#!bin/bash
current_path="$PWD"
echo "Prepare for cleaning data in ${current_path}"
sleep 1
echo "Stopping containers"
docker compose stop
echo "Cleaning services and containers exited..."
sleep 5
docker system prune
sleep 1
echo "Removing all images..."
docker rmi $(docker images -a -q)
sleep 1
echo "FINISHED"
