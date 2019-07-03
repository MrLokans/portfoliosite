FROM python:3.6.8-alpine AS builder
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

FROM python:3.6.8-alpine
HEALTHCHECK --interval=1m CMD curl --fail http://localhost:8000/api/health/ || exit 1
ENV PYTHONBUFFERED 1
COPY --from=builder /usr/local/bin/dumb-init /usr/local/bin/dumb-init
RUN adduser -D -g '' bloguser
RUN apk update \
    # Cron setup
    && apk add --no-cache -X http://dl-cdn.alpinelinux.org/alpine/edge/testing gdal proj-dev \
    && apk add dcron postgresql-dev jpeg-dev zlib-dev \
    && mkdir -p /var/log/cron \
    && mkdir -m 0644 -p /var/spool/cron/crontabs \
    && touch /var/log/cron/cron.log \
    && mkdir -m 0644 -p /etc/cron.d \
    # Install additional requirements
    && apk add bash git libxslt-dev libxml2-dev

COPY --from=builder /app/requirements.txt /app/requirements.txt
COPY --from=builder /root/.cache /root/.cache
RUN pip install -r /app/requirements.txt
COPY deployment/crontab /etc/cron.d/bloguser
ADD deployment/entrypoint.sh /docker-entrypoint.sh

RUN ln -s /usr/lib/libgeos_c.so.1.11.1 /usr/local/lib/libgeos_c.so.1
RUN ln -s /usr/lib/libgdal.so.20 /usr/local/lib/libgdal.so
RUN chmod +x /docker-entrypoint.sh
ENV GDAL_LIBRARY_PATH=/usr/lib/libgdal.so.20
ENV GEOS_LIBRARY_PATH=/usr/local/lib/libgeos_c.so.1
ENTRYPOINT ["/usr/local/bin/dumb-init", "--", "/docker-entrypoint.sh"]
