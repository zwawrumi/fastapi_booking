FROM python:3.12

RUN mkdir /booking_app

WORKDIR /booking_app

COPY requirements.txt .

COPY . .



