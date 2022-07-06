#!/bin/bash

python manage.py migrate
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata cookbook
sleep 5
yes | python manage.py search_index --rebuild
gunicorn redis_tutorial.wsgi:application --bind 0.0.0.0:8000 --reload

