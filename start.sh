#!/bin/bash
python manage.py migrate
python manage.py collectstatic --no-input
gunicorn bookstore.wsgi:application --bind 0.0.0.0:$PORT
