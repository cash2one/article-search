#!/bin/bash

WORK_DIR=`pwd`
DOMAIN_NAME="article-manager.zuoyetong.com.cn"
SRC_DIR="${WORK_DIR}/ng-app"
DEST_DIR="${WORK_DIR}/site/ng-dist/app"
EXT_PATTERN=".*\(\.js\|\.css\|\.html\|\.map\)"
INCLUDE_PATTERN=".*webfont.*"
SERVER_KEY_DIR="${WORK_DIR}/nginx/sslkey"
WEB_DOCKER_NAME="articlemanager_web"

# build node_module & grunt
rm -rf ${DEST_DIR} && mkdir -p ${DEST_DIR} && cd ${SRC_DIR}
npm install
grunt
cd -

# copy files
cd ${SRC_DIR}/app
find . -type d -name '*' -exec mkdir -p ${DEST_DIR}/{} \;
find . -type f -iregex ${EXT_PATTERN} -exec cp {} ${DEST_DIR}/{} \;
find . -type f -iregex ${INCLUDE_PATTERN} -exec cp {} ${DEST_DIR}/{} \;
cd -

# build web dcoker image
FINDER=`docker images | grep ${WEB_DOCKER_NAME}`
if [ "$FINDER" == "" ]; then
    docker build -t ${WEB_DOCKER_NAME} ${WORK_DIR}
fi

# collect all static files
STATIC_DIR=${WORK_DIR}/site/static
if [ ! -d "${STATIC_DIR}" ]; then
    mkdir -p ${STATIC_DIR} 
fi
MEDIA_DIR=${WORK_DIR}/site/media
if [ ! -d "${MEDIA_DIR}" ]; then
    mkdir -p ${MEDIA_DIR} 
fi 
echo 'collect static files'
docker run --rm \
           -v ${WORK_DIR}/site:/code \
           ${WEB_DOCKER_NAME} \
           python manage.py collectstatic --clear --noinput

# gen server key
if [ ! -d "${SERVER_KEY_DIR}" ]; then
    mkdir -p ${SERVER_KEY_DIR} 
fi 
cd ${SERVER_KEY_DIR}
if [ ! -f "${DOMAIN_NAME}.key" ]; then
    echo "generate new sslkey" 
    openssl req -x509 -newkey rsa:4086 -keyout ${DOMAIN_NAME}.key -out ${DOMAIN_NAME}.crt -days 3650 -nodes
else
    echo "use cached sslkey" 
fi
cd -
