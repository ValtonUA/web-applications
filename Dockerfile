FROM python:3.8

MAINTAINER Valentyn Telman

WORKDIR /django_project

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /django_project