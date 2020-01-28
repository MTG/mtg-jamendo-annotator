FROM python:3.7

ENV PYTHONUNBUFFERED=1

RUN mkdir /app
ADD requirements.txt /app

WORKDIR /app
RUN pip install --no-cache -r requirements.txt

ADD . /app