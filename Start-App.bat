@echo off
title DK Fashions - Server
cd /d "%~dp0"
echo Starting DK Fashions at http://127.0.0.1:8000/
start "" http://127.0.0.1:8000/
"C:\Users\redee\anaconda3\python.exe" manage.py runserver 127.0.0.1:8000
