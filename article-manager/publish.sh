#!/bin/bash

WORK_DIR=`pwd`
SRC_DIR="${WORK_DIR}/ng-app/app"
DEST_DIR="${WORK_DIR}/site/ng-dist/app"
EXT_PATTERN=".*\(\.js\|\.css\|\.html\|\.map\)"
INCLUDE_PATTERN=".*webfont.*"

rm -rf ${DEST_DIR} && mkdir -p ${DEST_DIR} && cd ${SRC_DIR}
grunt
find . -type d -name '*' -exec mkdir -p ${DEST_DIR}/{} \;
find . -type f -iregex ${EXT_PATTERN} -exec cp {} ${DEST_DIR}/{} \;
find . -type f -iregex ${INCLUDE_PATTERN} -exec cp {} ${DEST_DIR}/{} \;
cd -

# collect all static files
cd "${WORK_DIR}/site"
python manage.py collectstatic
cd -

# clean job
# rm -rf ${DEST_DIR}
