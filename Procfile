release: python manage.py migrate
workers: python manage.py rundramatiq -p1 -t1
web: gunicorn config.wsgi