#!/bin/bash
set -e

python manage.py makemigrations
python manage.py migrate --run-syncdb
python manage.py loaddata about_me/fixtures/fixtures.yaml
python manage.py collectstatic --no-input
gunicorn -w 4 -b :8000 personal_site.wsgi:application --reload