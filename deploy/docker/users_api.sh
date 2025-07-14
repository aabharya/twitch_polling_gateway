#!/bin/bash
export DJANGO_SETTINGS_MODULE=root.settings.prod
python3 manage.py check --deploy
python3 manage.py migrate --noinput
gunicorn --config ./root/gunicorn.py
