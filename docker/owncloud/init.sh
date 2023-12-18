docker run --rm -it \
	--user 1000:100 \
	-v $(pwd)/config:/etc/ocis \
	owncloud/ocis init
