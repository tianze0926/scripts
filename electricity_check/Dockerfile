# syntax=docker/dockerfile:1

FROM rust:alpine as builder
WORKDIR /app
COPY . .
RUN apk add --no-cache musl-dev openssl-dev
RUN cargo build --release

FROM alpine
COPY --from=builder /app/target/release/electricity_check /usr/local/bin/electricity_check

ENV MYHOME_USERNAME=
ENV MYHOME_PASSWORD=
ENV MYHOME_REMAIN_THRESHOLD=
ENV MYHOME_MONEY=
ENV EMAIL_FROM=
ENV EMAIL_TO=
ENV EMAIL_SUBJECT=
ENV EMAIL_BODY=
ENV SMTP_SERVER=
ENV SMTP_USERNAME=
ENV SMTP_PASSWORD=
ENV SMTP_PORT=
ENV CHECK_PERIOD=
ENV RETRY_PERIOD=

CMD /usr/local/bin/electricity_check
