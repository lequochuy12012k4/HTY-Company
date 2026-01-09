@echo off
echo Cloning repository...
git clone https://github.com/lequochuy12012k4/HTY-Company
echo Installing Python requirements...
pip install -r requirements.txt
echo Migrate to database
python manage.py makemigrations
python manage.py migrate
echo Setup complete.
echo Server is running at http://127.0.0.1:8000/
python manage.py runserver
pause