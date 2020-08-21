#!/bin/sh
pip install -r /app/requirements-dev.txt --progress-bar off
TESTING=true python -m pytest
