FROM python:3.9-slim

WORKDIR /dopomoga

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

RUN python manage.py makemessages -l uk && python manage.py compilemessages

CMD gunicorn --worker-tmp-dir /dev/shm dopomoga2.wsgi