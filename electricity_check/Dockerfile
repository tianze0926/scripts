# syntax=docker/dockerfile:1

FROM rust:alpine
WORKDIR /app
COPY . .
RUN cargo build --release
RUN ./target/release/electricity_check
