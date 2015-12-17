#!/bin/bash

DOWNLOAD_DIR=tarballs/

function install_mongodb() {
    local NEW_OR_OLD=$1
    local VER=$2
    wget -P $DOWNLOAD_DIR https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-$VER.tgz
    tar xvf $DOWNLOAD_DIR/mongodb-linux-x86_64-$VER.tgz
    mv mongodb-linux-x86_64-$VER $NEW_OR_OLD
}

rm $DOWNLOAD_DIR/* 
rm -rf {new,old}
install_mongodb old 2.4.12
install_mongodb new 2.6.7
sudo yum -y install tmux
