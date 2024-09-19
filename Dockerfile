# pull official base image
FROM python:3.11

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set default shell
SHELL [ "/bin/bash", "-c" ]

# set work directory
WORKDIR /app

# update/upgrade container & install git
RUN apt update && apt upgrade -y

# copy code files into container
COPY . .

# install required packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run server and Worker
RUN chmod +x /app/entrypoints/entrypoint.sh