FROM ubuntu:18.04

# LABEL maintainer="energieplanspiel"

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV POSTGRES_PASSWORD password
ENV POSTGRES_USER admin
ENV POSTGRES_DB energieplanspiel_db

WORKDIR /app/backend

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get install -y python3.7
RUN apt-get install -y build-essential gcc libpq-dev python-dev python3-dev python3.7-dev musl-dev libffi-dev git g++ make python-pip python3-pip postgresql-client coinor-cbc coinor-libcbc-dev libyaml-dev

COPY requirements.txt .

RUN pip install -U pip
RUN python3.7 -m pip install --upgrade pip
RUN pip install --no-cache-dir wheel psycopg2-binary
RUN pip install gunicorn
RUN pip install --no-cache-dir -r requirements.txt --no-deps --disable-pip-version-check

COPY . .

EXPOSE 8000

RUN python3.7 manage.py makemigrations

CMD python3.7 manage.py migrate && gunicorn backend.wsgi --bind 0.0.0.0:8000