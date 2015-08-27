#!/bin/bash

python makemigrations
python migrate

uwsgi --ini uwsgi.ini
