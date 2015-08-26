#!/bin/bash

if [ "$1" == "" ]; then
    echo 'usage : import.sh <elasticsearch_docker_name>'
    exit 1
fi

ES_CONTAINER_NAME=$1
MYSQL_DB_HOST="180.150.190.50"

docker run -d --link=$ES_CONTAINER_NAME:elasticsearch \
       -e "IMPORTER_DB_NAME=composition" \
       -e "IMPORTER_DB_HOST=$MYSQL_DB_HOST" \
       -e "IMPORTER_DB_PORT=3306" \
       -e "IMPORTER_DB_USER=lanbijia" \
       -e "IMPORTER_DB_PASSWORD=bijia@zyt_2015" \
       db_importer

