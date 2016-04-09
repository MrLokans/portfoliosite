FROM python:2.7

RUN apt-get update && apt-get install -y openssh-server \
&& apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false -o APT::AutoRemove::SuggestsImportant=false $buildDeps

COPY ./personal_site/requirements.txt ./requirements.txt

RUN pip install -r requirements.txt