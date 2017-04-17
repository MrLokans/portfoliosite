FROM python:3.5
ENV PYTHONBUFFERED 1
RUN adduser --disabled-password --gecos '' bloguser  
COPY requirements/base-requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
HEALTHCHECK --interval=20s --timeout=3s \
  CMD curl -f http://localhost:8000/api/healthcheck || exit 1