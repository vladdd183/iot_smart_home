sudo docker system prune -a

sudo docker volume ls -q | xargs sudo docker volume rm

sudo docker-compose up --build --force-recreate
