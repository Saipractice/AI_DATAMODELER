FROM ubuntu:18.04

ENV pythonunbuffered 1

FROM public.ecr.aws/docker/library/python:3.9.10-slim-buster
# Add SQL Server ODBC Driver
RUN apt-get update
RUN apt-get install -y curl gnupg
RUN curl -sSL https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl -sSL https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql18

RUN mkdir /AI-DATAMODELER

WORKDIR /AI-DATAMODELER

ADD . /AI-DATAMODELER


RUN pip install -r requirements.txt

EXPOSE 8000

CMD run uvicorn main:app --host 0.0.0.0 --port 8000