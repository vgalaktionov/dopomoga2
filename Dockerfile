FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y git gettext libgettextpo-dev binutils libproj-dev gdal-bin postgis

WORKDIR /dopomoga

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

RUN python manage.py makemessages -l uk && python manage.py compilemessages

CMD python manage.py collectstatic --noinput && python manage.py migrate && gunicorn --worker-tmp-dir /dev/shm dopomoga2.wsgi