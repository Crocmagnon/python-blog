#!/bin/sh
TESTING=true python -m pytest
pre-commit run --all-files
TESTING=true python manage.py makemigrations --check
