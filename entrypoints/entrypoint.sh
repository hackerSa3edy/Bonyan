#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Run database migrations
python manage.py makemigrations
python manage.py migrate

# Collect static files (if applicable)
python manage.py collectstatic --noinput

# Start the Gunicorn server
# exec gunicorn bonyanAuthService.wsgi:application --bind 0.0.0.0:80 --reload
python manage.py runserver 0.0.0.0:80