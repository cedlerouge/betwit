#!/bin/bash

# Set program name variable
prog=$0

function usage {
echo "usage: $prog [OPTIONS]"
    echo "Clean project environment and load fixtures"
    echo ""
    echo "OPTIONS"
    echo "  -p              put in prod or preprod  (default: false)"
    echo ""
    echo "EXAMPLES"
    echo ""
    echo "Clean project environment and load fixtures in dev mode"
    echo "  $prog"
    echo "Clean project environment and load fixtures in dev mode"
    echo "i.e : "
    echo "  - clean db"
    echo "  - load fixtures"
    echo "  - set local host as smtpout"
    echo "  $prog -p"
}

# Reset OPTIND
OPTIND=1

# Init
PROD=false

while getopts ":ph" opt; do
    case $opt in 
        p   ) PROD=true ;;
        h|* ) usage; exit 1;;
    esac
done

shift $((OPTIND-1))

initial_path=$(pwd)
dir=$(dirname $prog)

cd $dir
echo "Deleting migations files"
find ../ -path "*/migrations/*.py" -not -name "__init__.py" -delete
find ../ -path "*/migrations/*.pyc"  -delete                       
find ../ -name db.sqlite3 -delete
cd ../
# define smtpout if needed
if [ $PROD ]; then
    echo "Production ready: define localhost as smtpout"
    sed -i 's/^EMAIL_BACKEND.*/EMAIL_HOST = "localhost"\nEMAIL_PORT = 25\nDEFAULT_FROM_EMAIL = "betwit@lepont.bzh"/' ./betwit/setting.py
    sed -i 's/^DEBUG = True/DEBUG = False/' ./betwit/setting.py
    key==$(</dev/urandom tr -dc A-KM-NP-Za-km-z2-9.\;\!:/\*$+-, | head -c 50)
    sed -i "s/^SECRET_KEY = .*/SECRET_KEY = '$key'/" ./betwit/setting.py
fi

echo "Installing modules"
pip install -q -r requirements.txt
echo "Create migrations files"
python manage.py makemigrations
echo "Migrate db"
python manage.py migrate
echo "Create superuser"
#python manage.py createsuperuser
python manage.py loaddata ./*/fixtures/*.json
cd $initial_path
echo "You can now launch application: python manage.py runserver"
exit 0
