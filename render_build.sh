#!/usr/bin/env bash
set -o errexit

pipenv install

pipenv run upgrade

pipenv run flask --app src/app.py seed
