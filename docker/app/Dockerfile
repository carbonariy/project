FROM python:3.12-bookworm
ENV PYTHONUNBUFFERED 1
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /code

RUN apt-get update && apt-get install --no-install-recommends -y  \
    supervisor \
    build-essential
RUN pip install --upgrade pip uwsgi poetry

ADD docker/app/supervisor-app.conf /etc/supervisor/conf.d/
ADD docker/app/uwsgi.ini /etc/uwsgi.ini

ADD pyproject.toml /code/
ADD poetry.lock /code/
RUN poetry install --no-interaction --no-ansi

ADD backend /code/

RUN mkdir -p /code/logs/
RUN mkdir -p /code/media/
RUN mkdir -p /code/static/
RUN python manage.py collectstatic --noinput
