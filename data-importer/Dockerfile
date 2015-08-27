FROM python:2.7
MAINTAINER "Bijia Lan <lbj.world@gmail.com>"

# setup env
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt

# run job
CMD python import_files.py 
