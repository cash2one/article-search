FROM python:2.7
MAINTAINER "Bijia Lan <lbj.world@gmail.com>"

ENV SERVICE_PORT 8000
ADD ./site /code
WORKDIR /code

RUN pip install -r requirements.txt

EXPOSE $SERVICE_PORT

CMD python manage.py migrate;uwsgi --ini uwsgi.ini
