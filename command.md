# new Django project named mysit
django-admin startproject mysite

# new Django application
python manage.py startapp blog


python -m pip install -r requirements.txt.

python3 -m venv my_env

source my_env/bin/activate

deactivate

python manage.py runserver 127.0.0.1:8001

# run the development server specifying host/port and settings file:
python manage.py runserver 127.0.0.1:8001 --settings=mysite.settings

## Blog Application commands
Post.Status.choices

Post.Status.name

Post.Status.labels

Post.Status.values

# To view the SQL statements that will be executed with the first migration of the blog application:
python manage.py sqlmigrate blog 0001


## send email using shell
from django.core.mail import send_mail
send_mail('Django mail','This e-mail was sent with Django.', 'from@gmail.com', ['to@gmail.com'], fail_silently=False)


## Pull docker image
docker pull postgres:16.2

## run postgresql service
docker run --name=blog_db -e POSRGRES_DB=blog -e POSTGRES_USER=blog -e POSTGRES_PASSWORD=xxxxx -p 5432:5432 -d postgres:16.2

## Dump data
python manage.py dumpdata --indent=2 --output=mysite_data.json
python -Xutf8 manage.py dumpdata --indent=2 --output=mysite_data.json

## Loading the data into the new database
python manage.py loaddata mysite_data.json