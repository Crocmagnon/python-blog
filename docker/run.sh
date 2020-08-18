#!/bin/sh
yes yes | python manage.py migrate \
&& python manage.py collectstatic --noinput --clear \
&& gunicorn blog.wsgi -b 0.0.0.0:8000 --log-file -
