# syntax=docker/dockerfile:1

FROM python:3.8-alpine
WORKDIR /usr/src/app

ENV AUTH_FILE=

COPY backup.py ./
VOLUME /file

RUN pip install requests
CMD python backup.py --auth_file $AUTH_FILE
