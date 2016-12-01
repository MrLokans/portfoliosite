FROM python:3.5
ENV PYTHONBUFFERED 1
COPY requirements/base-requirements.txt /app/requirements.txt
COPY entrypoint.sh /entrypoint.sh
RUN pip install -r /app/requirements.txt