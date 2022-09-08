# syntax=docker/dockerfile:1

FROM rust:alpine
WORKDIR /app
COPY . .
RUN apk add --no-cache openssl-dev
RUN cargo build --release
RUN ./target/release/electricity_check
