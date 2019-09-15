FROM personal_site_base:latest

COPY requirements/base.txt /app/base.txt
RUN pip install -r /app/base.txt
COPY deployment/crontab /etc/cron.d/bloguser
ADD deployment/entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
RUN useradd -ms /bin/bash bloguser
ADD ./apps/ /app/apps/
ADD ./personal_site/ /app/personal_site/
ADD ./deployment/gunicorn.conf /app//deployment/gunicorn.conf
ADD ./manage.py /app/manage.py
WORKDIR /app/
RUN apt-get update \
    && apt-get install -y --no-install-recommends gdal-bin cron \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /app/apps/about_me/fixtures

RUN chmod 0644 /etc/cron.d/bloguser
RUN crontab /etc/cron.d/bloguser
RUN touch /var/log/cron.log

ENTRYPOINT ["/usr/local/bin/dumb-init", "--", "/docker-entrypoint.sh"]
