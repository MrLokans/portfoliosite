FROM python:3.5
ENV PYTHONBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD personal_site/requirements.txt /code/
RUN pip install -r requirements.txt
ADD ./personal_site /code/