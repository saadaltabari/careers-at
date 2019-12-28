FROM python:3.7-alpine

MAINTAINER Saad Altabari

RUN apk --update add \
    build-base \
    mariadb-dev

ENV PYTHONUNBUFFERED 1

ENV FLASK_APP=app.py

ARG FLASK_ENV_ARG=development
ENV FLASK_ENV=$FLASK_ENV_ARG

COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir /app
RUN mkdir /uplods

COPY ./api /app
WORKDIR /app

RUN adduser -D app_user
RUN chown -R app_user: /app
RUN chmod -R u+w /app
USER app_user


EXPOSE 5000
CMD python -m flask run --host=0.0.0.0
