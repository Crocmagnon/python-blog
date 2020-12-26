#!/bin/bash
set -eux
yes yes | python manage.py migrate
python manage.py collectstatic --noinput --clear
python manage.py assets build --manifest django
gunicorn blog.wsgi -b 0.0.0.0:8000 --log-file -
