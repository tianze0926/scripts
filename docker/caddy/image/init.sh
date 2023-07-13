usermod --non-unique --uid $PUID abc
groupmod --non-unique --gid $PGID abc

chown --quiet -R $PUID:$PGID /app

runuser -u abc -- python convert/generate.py \
	--input_config caddy.yml \
	--input_sensitive_config sensitive.yml \
	--output_caddy_config caddy.json

runuser -u abc -- ./caddy \
	run --config caddy.json

# runuser -u abc -- "$@"
