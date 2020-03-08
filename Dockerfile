FROM registry.mrlokans.com:5000/personal_site_base:latest

COPY backend/requirements/base.txt /app/base.txt
RUN pip install -r /app/base.txt
ADD deployment/entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
RUN useradd -ms /bin/bash bloguser
ADD ./backend/apps/ /app/apps/
ADD ./backend/manage.py /app/manage.py
ADD ./deployment/gunicorn.conf /app/deployment/gunicorn.conf
WORKDIR /app/
RUN apt-get update \
    && apt-get install -y --no-install-recommends gdal-bin osmctools osm2pgsql \
    && rm -rf /var/lib/apt/lists/*
ENTRYPOINT ["/usr/local/bin/dumb-init", "--", "/docker-entrypoint.sh"]
