#!/bin/bash
set -e

BACKEND_USER=bloguser


echo "Launching cron"

[ "$(ls -A /etc/cron.d)" ] && cp -f /etc/cron.d/* /var/spool/cron/crontabs/$BACKEND_USER || true
crond -s /var/spool/cron/crontabs -f -L /var/log/cron/cron.log &

echo "Applying migrations"
su "$BACKEND_USER" -c "python manage.py makemigrations"
su "$BACKEND_USER" -c "python manage.py migrate --run-syncdb"
echo "Loading initial fixtures"
su "$BACKEND_USER" -c "python manage.py loaddata about_me/fixtures/fixtures.yaml"
echo "Collecting static"
# chown -R $BACKEND_USER:$BACKEND_USER static
python manage.py collectstatic --no-input

if [[ $@ == **prod** ]]
then
    echo "Using prod configuration."
    su "$BACKEND_USER" -c "gunicorn -w 4 -b :8000 personal_site.wsgi:application --access-logfile - --error-logfile -"
else
    echo "Using dev configuration"
    su "$BACKEND_USER" -c "gunicorn -w 4 -b :8000 personal_site.wsgi:application --reload"
fi