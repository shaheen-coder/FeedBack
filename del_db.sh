rm db.sqlite3
cd core/migrations 
rm *.py
cd __pycache__
rm *.pyc
echo "\n deletion done ";

python manage.py makemigrations core

echo "\n Migrations done \n";

python manage.py migrate

echo "\n migrate done\n";
clear

python manage.py createsuperuser

clear
echo "everything is done";

