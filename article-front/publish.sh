#!/bin/bash

WORK_DIR=`pwd`
DOMAIN_NAME="article-front.zuoyetong.com.cn"
SRC_DIR="${WORK_DIR}/ng-app"
DEST_DIR="${WORK_DIR}/site/app"
EXT_PATTERN=".*\(\.min\.js\|\.css\|\.html\|\.map\)"
SERVER_KEY_DIR=${WORK_DIR}/nginx/sslkey

# build node_module & grunt
rm -rf ${DEST_DIR} && mkdir -p ${DEST_DIR} && cd ${SRC_DIR}
npm install
grunt
cd -

# copy files
cd ${SRC_DIR}/app
find . -type d -name '*' -exec mkdir -p ${DEST_DIR}/{} \;
find . -type f -iregex ${EXT_PATTERN} -exec cp {} ${DEST_DIR}/{} \;
cd -

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
