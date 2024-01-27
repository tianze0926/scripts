docker compose run -it --rm \
	-v $(pwd)/data:/data \
	-e SYNAPSE_SERVER_NAME=tianze.me \
	-e SYNAPSE_REPORT_STATS=no \
	--user 1000:100 \
	server generate
