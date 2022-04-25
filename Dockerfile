FROM python:3.9-slim

WORKDIR /dopomoga

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

CMD gunicorn dopomoga2.wsgi