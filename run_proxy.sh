#!/usr/bin/env bash

export DOCKER_BUILDKIT=1
FRONTEND_LOCAL_PORT=3000
BACKEND_LOCAL_PORT=8000
LOCAL_DOMAIN_NAME=mrlokans.qa

if ! grep -q $LOCAL_DOMAIN_NAME /etc/hosts
then
  echo "There is no '$LOCAL_DOMAIN_NAME' in /etc/hosts. Please include it for proxy to work properly."
  exit 1
else
  echo "/etc/hosts has '$LOCAL_DOMAIN_NAME' entry, proceeding"
fi

docker build -f Dockerfile.local.nginx . --tag local-proxy

echo "Running proxy on $LOCAL_DOMAIN_NAME"
docker run -t --rm -p 80:80 local-proxy
