sudo docker system prune -a
sudo docker ps -a | awk '{print $1}' | tac | head -n -1 | xargs sudo docker stop | xargs sudo docker rm

sudo docker volume ls -q | xargs sudo docker volume rm

sudo docker-compose up --build # --force-recreate
