#!/usr/bin/env bash
set -o errexit

python -m pip install --upgrade pip pipenv

pipenv install --system --deploy

flask --app src/app.py db upgrade

flask --app src/app.py seed
