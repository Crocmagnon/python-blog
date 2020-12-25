#!/bin/sh
set -euxo pipefail
python -m pytest
pre-commit run --all-files
python manage.py makemigrations --check
