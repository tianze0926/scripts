FROM nerd.us.leous.eu.org:1111/tianze0926/caddy

ARG PUID
ARG PGID

USER root
RUN usermod --non-unique --uid $PUID abc &&\
    groupmod --non-unique --gid $PGID abc &&\
    chown --quiet -R $PUID:$PGID /app

USER abc

