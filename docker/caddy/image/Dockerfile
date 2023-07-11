FROM golang:1.19-bullseye as builder
WORKDIR /app
ARG CADDY_VERSION=latest
RUN go install github.com/caddyserver/xcaddy/cmd/xcaddy@latest; \
    xcaddy build $CADDY_VERSION \
        --with github.com/caddy-dns/cloudflare \
        --output caddy


FROM debian:bullseye-slim
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update; \
    apt-get install -y ca-certificates
WORKDIR /app
COPY --from=builder /app/caddy .

ENV XDG_CONFIG_HOME /app/config
ENV XDG_DATA_HOME /app/data

RUN useradd -m -U abc
COPY init.sh .

RUN apt-get clean

STOPSIGNAL SIGINT
ENTRYPOINT ["/bin/sh", "/app/init.sh"]
