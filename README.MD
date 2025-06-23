https://medium.com/@codingwitharyan/introduction-to-django-for-backend-development-2db67768ee62

## start a django app 
python manage.py startapp appname

afterwards add to INSTALLED_APPS in project > settings.py

## start a django project (projects > apps)
django-admin startproject 

## After adding model orm
python manage.py makemigrations

-> to map sql commands

python manage.py migrate