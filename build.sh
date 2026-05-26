#!/usr/bin/env bash

cd config

pip install -r ../requirements.txt

python manage.py collectstatic --noinput

python manage.py migrate