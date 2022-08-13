#!/usr/bin/env bash
poetry run python manage.py makemigrations
poetry run python manage.py migrate 
poetry run python -u manage.py runserver 0.0.0.0:8000
