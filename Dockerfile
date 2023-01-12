FROM python:3.8

MAINTAINER khk37601@gmail.com

RUN mkdir /var/log/hometax

COPY . /app

WORKDIR /app

RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt

ENV PYTHONPATH=/app


EXPOSE 80
