# syntax=docker/dockerfile:1

FROM python:3.8-alpine

WORKDIR /usr/src/app

COPY backup.py ./
VOLUME /file

ENV AUTH_FILE=

CMD python backup.py --auth_file $AUTH_FILE
