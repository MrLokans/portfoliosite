FROM python:3.6.1-alpine AS builder
COPY requirements/base.txt /app/requirements.txt
RUN apk update && apk add --no-cache libffi libxslt postgresql-dev \
    && apk add --virtual build-dependencies --no-cache \
        git gcc linux-headers \
        musl-dev libxml2-dev \
        jpeg-dev zlib-dev libxslt-dev \
        libffi-dev openssl-dev openssl\
    && LIBRARY_PATH=/lib:/usr/lib pip install -r /app/requirements.txt
RUN wget -O /usr/local/bin/dumb-init https://github.com/Yelp/dumb-init/releases/download/v1.2.1/dumb-init_1.2.1_amd64
RUN chmod +x /usr/local/bin/dumb-init

FROM python:3.6.1-alpine
HEALTHCHECK --interval=1m CMD curl --fail http://localhost:8000/api/health/ || exit 1
ENV PYTHONBUFFERED 1
COPY --from=builder /usr/local/bin/dumb-init /usr/local/bin/dumb-init
RUN adduser -D -g '' bloguser
RUN apk update \
    # Cron setup
    && apk add dcron postgresql-dev \
    && mkdir -p /var/log/cron \
    && mkdir -m 0644 -p /var/spool/cron/crontabs \
    && touch /var/log/cron/cron.log \
    && mkdir -m 0644 -p /etc/cron.d \
    # Install additional requirements
    && apk add bash git
COPY --from=builder /app/requirements.txt /app/requirements.txt
COPY --from=builder /root/.cache /root/.cache
RUN pip install -r /app/requirements.txt
COPY crontab /etc/cron.d/bloguser
ADD entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/usr/local/bin/dumb-init", "--", "/docker-entrypoint.sh"]