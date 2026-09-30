#!/bin/bash
# Vercel build step: install deps and collect static files into staticfiles/.
pip install -r requirements.txt
python3.12 manage.py collectstatic --noinput --clear
