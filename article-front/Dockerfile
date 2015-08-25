FROM python:2.7

ADD ./site /code
WORKDIR /code

ENV PYCURL_SSL_LIBRARY openssl
RUN pip install -r requirements.txt

EXPOSE 5000

CMD python web_app.py port 5000 debug 0 
