FROM python:alpine

EXPOSE 5000

RUN apk add build-base

WORKDIR app

COPY * /app/

RUN pip install -r requirements.txt

ENV FLASK_APP=procrastinator
ENV FLASK_ENV=development
CMD flask run -h 0.0.0.0
