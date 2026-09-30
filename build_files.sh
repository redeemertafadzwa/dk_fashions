#!/bin/bash
# Vercel build step: install deps, collect static, and set up the database.
set -e

pip install -r requirements.txt

python3.12 manage.py collectstatic --noinput --clear

# Set up the hosted database on each deploy (all idempotent).
python3.12 manage.py migrate --noinput
python3.12 manage.py seed
python3.12 manage.py bootstrap_admin
