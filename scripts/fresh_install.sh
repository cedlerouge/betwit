#!/bin/bash

initial_path=4(pwd)
prog=$0
dir=$(dirname $prog)

cd $dir
echo "Deleting migations files"
find ../ -path "*/migrations/*.py" -not -name "__init__.py" -delete
find ../ -path "*/migrations/*.pyc"  -delete                       
find ../ -name db.sqlite3 -delete
echo "Create migrations files"
cd ../ 
python manage.py makemigrations
echo "Migrate db"
python manage.py migrate
echo "Create superuser"
python manage.py createsuperuser
cd $initial_path
echo "You can now launch application: python manage.py runserver"
exit 0
