#!/usr/bin/env bash

set -e

BACKEND_USER=bloguser
GUNICORN_WORKERS=${GUNICORN_WORKERS:-4}
GUNICORN_PORT=${GUNICORN_PORT:-8000}

echo "Launching cron"
cron -f &

echo "Applying migrations"
su "$BACKEND_USER" -c "python manage.py migrate"
echo "Collecting static (output dir: $DJANGO_STATIC_DIR)"
python manage.py collectstatic --no-input

if [[ $@ == **prod** ]]
then
    echo "Using prod configuration."
    gunicorn --log-config deployment/gunicorn.conf -w $GUNICORN_WORKERS -b :$GUNICORN_PORT personal_site.wsgi:application -u $BACKEND_USER
else
    echo "Using dev configuration"
    gunicorn --log-config deployment/gunicorn.conf -w $GUNICORN_WORKERS -b :$GUNICORN_PORT personal_site.wsgi:application --reload -u $BACKEND_USER
fi