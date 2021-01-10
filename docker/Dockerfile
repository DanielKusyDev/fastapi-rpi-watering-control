FROM python:3.8.5-slim

ENV APP_DIR /app

RUN mkdir $APP_DIR
WORKDIR $APP_DIR

RUN apt update

RUN apt install -y gcc make

RUN pip install -U setuptools

COPY ./requirements.txt $APP_DIR/
RUN pip3 install -r requirements.txt
