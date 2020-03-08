#!/usr/bin/env bash

set -e

BACKEND_USER=bloguser
GUNICORN_WORKERS=${GUNICORN_WORKERS:-4}
GUNICORN_PORT=${GUNICORN_PORT:-8000}

echo "Applying migrations"
su "$BACKEND_USER" -c "python manage.py migrate"
echo "Collecting static (output dir: $DJANGO_STATIC_DIR)"
python manage.py collectstatic --no-input

if [[ $@ == **prod** ]]; then
    echo "Web-application in prod configuration."
    gunicorn --log-config deployment/gunicorn.conf -w $GUNICORN_WORKERS -b :$GUNICORN_PORT apps.core.wsgi:application -u $BACKEND_USER
elif [[ $@ == **bot** ]]; then
    echo "Running telegram bot."
    python manage.py run_apartments_bot
else
    echo "Web-application in dev configuration"
    gunicorn --log-config deployment/gunicorn.conf -w $GUNICORN_WORKERS -b :$GUNICORN_PORT apps.core.wsgi:application --reload -u $BACKEND_USER
fi
