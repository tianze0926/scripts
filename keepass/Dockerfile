# syntax=docker/dockerfile:1

FROM python:3.8-alpine
WORKDIR /usr/src/app

ENV AUTH_FILE=

COPY backup.py ./
RUN mkdir /file

RUN pip install requests
CMD python -t backup.py --auth_file $AUTH_FILE
