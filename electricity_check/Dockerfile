# syntax=docker/dockerfile:1

FROM rust:alpine as builder
WORKDIR /app
COPY . .
RUN apk add --no-cache musl-dev openssl-dev
RUN cargo build --release

FROM alpine
COPY --from=builder /app/target/release/electricity_check /usr/local/bin/electricity_check
CMD /usr/local/bin/electricity_check
