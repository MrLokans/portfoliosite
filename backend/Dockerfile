FROM python:3.6.1-alpine
HEALTHCHECK --interval=1m CMD curl --fail http://localhost:8000/api/health/ || exit 1
ENV PYTHONBUFFERED 1
RUN adduser -D -g '' bloguser
RUN apk update \
    # Cron setup
    && apk add dcron \
    && mkdir -p /var/log/cron \
    && mkdir -m 0644 -p /var/spool/cron/crontabs \
    && touch /var/log/cron/cron.log \
    && mkdir -m 0644 -p /etc/cron.d
COPY requirements/base-requirements.txt /app/requirements.txt
RUN apk add --no-cache bash curl libffi postgresql-dev \
    && apk add --virtual build-dependencies --no-cache \
        git gcc linux-headers \
        musl-dev  libxslt libxml2-dev \
        jpeg-dev zlib-dev libxslt-dev \
        libffi-dev openssl-dev \
    && LIBRARY_PATH=/lib:/usr/lib pip install -r /app/requirements.txt \
    && apk del build-dependencies
COPY crontab /etc/cron.d/bloguser