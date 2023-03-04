FROM python:3.10
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive
WORKDIR /code
RUN apt-get update && apt-get install --no-install-recommends -y supervisor
RUN pip install --upgrade pip uwsgi
ADD docker/app/supervisor-app.conf /etc/supervisor/conf.d/
ADD docker/app/uwsgi.ini /etc/uwsgi.ini
ADD backend/requirements.txt /code/
RUN pip install -r requirements.txt
ADD backend /code/
RUN mkdir -p /code/logs/
RUN mkdir -p /code/media/
RUN mkdir -p /code/static/
