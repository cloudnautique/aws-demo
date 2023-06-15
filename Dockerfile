# create a dockerfile for a python flask app

# use the official Python image
FROM python:3-alpine

ADD . /app
RUN apk add --update --no-cache gcc musl-dev mariadb-connector-c-dev && \
    pip install -r /app/requirements.txt


ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

WORKDir /app
EXPOSE 5000

CMD ["flask", "--debug", "run"]