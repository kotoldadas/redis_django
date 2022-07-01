#!/bin/bash

python manage.py migrate
python manage.py makemigrations
python manage.py loaddata cookbook
gunicorn redis_tutorial.wsgi:application --bind 0.0.0.0:8000

