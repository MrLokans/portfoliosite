#!/bin/bash
set -e

python manage.py loaddata about_me/fixtures/fixtures.yaml
python manage.py collectstatic --no-input
python manage.py migrate
gunicorn -w 4 -b :8000 personal_site.wsgi:application --reload