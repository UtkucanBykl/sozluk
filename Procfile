release: python manage.py migrate && python manage.py create_basic_admin
dramatiq: python manage.py rundramatiq -p1 -t1
web: gunicorn config.wsgi