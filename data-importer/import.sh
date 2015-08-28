#!/bin/bash

function error() {
    echo $1
    echo "usage : import.sh <elasticsearch_docker_name> <db_source:[mofangge|backend]> [db_docker_name]"
    exit 1
}

function import_mofangge_db() {
    docker run --link=$1:elasticsearch \
           -e "IMPORTER_DB_NAME=composition" \
           -e "IMPORTER_DB_HOST=$2" \
           -e "IMPORTER_DB_PORT=3306" \
           -e "IMPORTER_DB_USER=lanbijia" \
           -e "IMPORTER_DB_PASSWORD=bijia@zyt_2015" \
           db_importer python import_mofangge_db.py
}

function import_backend_db() {
    docker run --link=$1:elasticsearch --link=$2:db \
           -e "IMPORTER_DB_NAME=articles" \
           -e "IMPORTER_DB_HOST=db" \
           -e "IMPORTER_DB_PORT=3306" \
           -e "IMPORTER_DB_USER=root" \
           -e "IMPORTER_DB_PASSWORD=docker-mysql" \
           db_importer python import_backend_db.py
}

if [[ "$1" == "" ]]; then
    error "please input <elasticsearch_docker_name>"
fi
if [[ "$2" == "" ]]; then
    error "please input <db_source>"
fi

ES_CONTAINER_NAME=$1
DB_CONTAINER_NAME=$3
MYSQL_MOFANGGE_DB_HOST="180.150.190.50"
MYSQL_MOFANGGE_DB_PWD="bijia@zyt_2015"

case $2 in
    "mofangge")
        import_mofangge_db $ES_CONTAINER_NAME $MYSQL_DB_HOST
        ;;
    "backend")
        import_backend_db $ES_CONTAINER_NAME $DB_CONTAINER_NAME
        ;;
    *)
        error "invalid db_source : $2"
        ;;
esac




