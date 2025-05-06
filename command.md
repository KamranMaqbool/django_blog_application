python -m pip install -r requirements.txt.

python3 -m venv my_env

source my_env/bin/activate

deactivate

python manage.py runserver 127.0.0.1:8001

python manage.py runserver 127.0.0.1:8001 --settings=mysite.settings

## Blog Application commands
Post.Status.choices

Post.Status.name

Post.Status.labels

Post.Status.values

python manage.py sqlmigrate blog 0001

