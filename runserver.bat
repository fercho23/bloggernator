@echo off

cd backend
CALL venv\Scripts\activate.bat
python manage.py runserver
cmd /k