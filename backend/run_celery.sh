#!/bin/sh

echo "Wating 10 seconds for the RabbitMQ server."
sleep 10

BLOG_USER=bloguser

# run Celery worker for our project myproject with Celery configuration stored in Celeryconf
su -m $BLOG_USER -c "celery worker -A celeryconfig -Q default -n default@%h"  