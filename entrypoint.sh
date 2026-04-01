#!/bin/bash

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Translations"
python manage.py compilemessages

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Run server
gunicorn config.wsgi:application -c gunicorn.conf.py
