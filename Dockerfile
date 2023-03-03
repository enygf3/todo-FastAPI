# Dockerfile, Image, Container
# syntax=docker/dockerfile:1

FROM python:3.11.2
WORKDIR .
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .