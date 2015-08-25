FROM python:2.7
ADD ./site /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD python web_app.py port 5000 debug 0 
