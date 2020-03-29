release: python manage.py migrate && python manage.py create_basic_admin
worker: python manage.py rundramatiq
web: gunicorn config.wsgi