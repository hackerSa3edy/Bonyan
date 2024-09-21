# pull official base image
FROM python:3.11-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# set default shell
SHELL ["/bin/bash", "-c"]

# set work directory
WORKDIR /app

# update/upgrade container & install dependencies
RUN apt-get update && apt-get upgrade -y

# copy code files into container
COPY . .

# ensure entrypoint script is present and executable
RUN chmod +x /app/entrypoints/backend_entrypoint.sh

# install required packages
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt