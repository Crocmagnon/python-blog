#!/bin/bash
set -eux
python manage.py migrate --noinput
python manage.py collectstatic --noinput --clear
gunicorn blog.wsgi -b 0.0.0.0:8000 --log-file -
