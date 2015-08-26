FROM python:2.7

# setup env
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt

# run job
CMD python import_db.py 
#CMD python import_files.py 
