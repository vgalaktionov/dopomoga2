FROM python:3.9-slim

WORKDIR /dopomoga

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

CMD gunicorn --worker-tmp-dir /dev/shm dopomoga2.wsgi