FROM owncloud/server:10.13

ARG PUID
ARG PGID

RUN usermod --non-unique --uid $PUID www-data &&\
    groupmod --non-unique --gid $PGID www-data &&\
    chown --quiet -R $PUID:$PGID /var/www/owncloud

