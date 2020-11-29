FROM python:3.8
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt --no-cache-dir -r /app/requirements.txt
COPY . /app/
ENV DJANGO_ENV=development
ENV REDIS_URL=redis://redis:6379
RUN ["chmod", "+x", "/app/docker/django.sh"]
