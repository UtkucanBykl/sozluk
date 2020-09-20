FROM python:3.8
WORKDIR /app
ADD . /app
ENV DJANGO_ENV=development
ENV REDIS_URL=redis://redis:6379
RUN pip install -r requirements.txt
