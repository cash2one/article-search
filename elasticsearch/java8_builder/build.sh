#!/bin/bash

if [ "$1" == "" ]; then
    echo 'usage : build.sh <git://plugin_url>'
    exit 1
fi

GIT_URL=$1
PLUGIN_NAME=${GIT_URL##*/}
TMP_DIR=`pwd`/build_tmp

mkdir -p $TMP_DIR && cd $TMP_DIR
WORK_DIR="$TMP_DIR/$PLUGIN_NAME"
if [ ! -d "$WORK_DIR" ]; then
    echo 'download plugin src from git'
    git clone ${GIT_URL}
else
    echo 'use plugin src cache'
fi 

BUILD_FILE=`find $WORK_DIR -name pom.xml`
BUILD_DIR=${BUILD_FILE%/*.xml}
if [ ! -d "$BUILD_DIR" ]; then
    echo 'error: cannot find plugin dir:'$WORK_DIR
    exit 1
fi
echo 'build plugin by using docker container'
sudo docker run --rm -it -v ${BUILD_DIR}:/tmp/build java_builder:latest mvn package

echo 'finish build'

