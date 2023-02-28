FROM mcr.microsoft.com/devcontainers/python:0-3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN export DJANGO_SETTINGS_MODULE="app.settings"

WORKDIR /app

RUN pip install --upgrade pip
COPY requirements.txt /app
RUN pip3 install -r requirements.txt --no-cache-dir

COPY . /app

EXPOSE 8000
