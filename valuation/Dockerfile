#FROM ubuntu:22.04
FROM python:3.9.20-slim-bullseye

WORKDIR /app

# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# RUN apt update &&\
#     apt install -y python3-pip

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app .