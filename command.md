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
