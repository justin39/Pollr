release: python manage.py migrate
web: gunicorn pollr.wsgi:application --log-file -
