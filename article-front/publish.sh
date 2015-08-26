#!/bin/bash

WORK_DIR=`pwd`
SRC_DIR="${WORK_DIR}/ng-app"
DEST_DIR="${WORK_DIR}/site/app"
EXT_PATTERN=".*\(\.min\.js\|\.css\|\.html\|\.map\)"

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

#openssl req -x509 -newkey rsa:4086 -keyout article-front.zuoyetong.com.cn.key -out article-front.zuoyetong.com.cn.crt -days 3650 -nodes
