FROM python:3.8.5-slim

ENV APP_DIR /app

RUN mkdir $APP_DIR
WORKDIR $APP_DIR

RUN apt update

COPY ./requirements.txt $APP_DIR/
RUN pip install -q -r requirements.txt
