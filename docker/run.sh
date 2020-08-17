#!/bin/sh
yes yes | python manage.py migrate && \
#yes yes | pipenv run python manage.py createcachetable && \
python manage.py collectstatic --noinput && \
gunicorn blog.wsgi -b 0.0.0.0:8000 --log-file -
