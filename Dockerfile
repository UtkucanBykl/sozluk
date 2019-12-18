FROM python:3.7
ADD . /app
WORKDIR /app
ENV DJANGO_ENV=development
RUN pip install -r req.txt
