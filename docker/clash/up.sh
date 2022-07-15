SECRET=$(cat sensitive_secret.txt)
SUB=$(cat sensitive_subscription.txt | sed -e 's/\//\\\//g' -e 's/\&/\\\&/g') # escape '/' and '&'

sed -e "s/{SECRET}/$SECRET/" \
    -e "s/{SUBSCRIPTION}/$SUB/" \
    config.yaml > sensitive_config.yaml

docker compose stop
docker compose up -d