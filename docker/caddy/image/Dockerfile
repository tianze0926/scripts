FROM golang:1.19-bullseye as builder
WORKDIR /app
ARG CADDY_VERSION=latest
RUN go install github.com/caddyserver/xcaddy/cmd/xcaddy@latest; \
    xcaddy build $CADDY_VERSION \
        --with github.com/caddy-dns/cloudflare \
        --output caddy


FROM python
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update &&\
    apt-get install -y ca-certificates &&\
    apt-get clean
WORKDIR /app

COPY --from=builder /app/caddy .
ENV XDG_CONFIG_HOME /app/config
ENV XDG_DATA_HOME /app/data

RUN useradd --create-home --user-group abc
USER abc
COPY convert/ ./convert/
RUN cd convert && pip install -r requirements.txt

USER root
COPY init.sh .

RUN 

STOPSIGNAL SIGINT
ENTRYPOINT ["/bin/sh", "/app/init.sh"]
