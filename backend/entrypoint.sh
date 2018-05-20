#!/usr/bin/env bash

set -e

BACKEND_USER=bloguser
GUNICORN_WORKERS=${GUNICORN_WORKERS:-4}
GUNICORN_PORT=${GUNICORN_PORT:-8000}

echo "Launching cron"
[ "$(ls -A /etc/cron.d)" ] && cp -f /etc/cron.d/* /var/spool/cron/crontabs/$BACKEND_USER || true
crond -s /var/spool/cron/crontabs -f -L /var/log/cron/cron.log &

echo "Applying migrations"
su "$BACKEND_USER" -c "python manage.py migrate --run-syncdb"
echo "Loading initial fixtures"
su "$BACKEND_USER" -c "python manage.py loaddata about_me/fixtures/fixtures.yaml"
echo "Collecting static (output dir: $DJANGO_STATIC_DIR)"
python manage.py collectstatic --no-input
chown -R $BACKEND_USER:$BACKEND_USER $DJANGO_STATIC_DIR

if [[ $@ == **prod** ]]
then
    echo "Using prod configuration."
    gunicorn --log-config gunicorn.conf -w $GUNICORN_WORKERS -b :$GUNICORN_PORT personal_site.wsgi:application --access-logfile - --error-logfile -u $BACKEND_USER
else
    echo "Using dev configuration"
    gunicorn --log-config gunicorn.conf -w $GUNICORN_WORKERS -b :$GUNICORN_PORT personal_site.wsgi:application --reload -u $BACKEND_USER
fi