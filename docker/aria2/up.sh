SECRET=$(cat sensitive_secret.txt | sed -e 's/\//\\\//g' -e 's/\&/\\\&/g') # escape '/' and '&'

sed -e "s/{SECRET}/$SECRET/" \
    docker-compose-example.yml > docker-compose.yml

docker compose stop
docker compose up -d