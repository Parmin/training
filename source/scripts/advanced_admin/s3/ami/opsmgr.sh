#!/bin/bash

### TODO
# - ability to download the 'datasets' and 'validation' scripts from a test location
# - test for error codes in running commands and return them to the caller!?

### Machine Role: OpsMgr and Node

### Files to download
DIR=/data/downloads
FILES=(
    https://downloads.mongodb.com/on-prem-mms/rpm/mongodb-mms-2.0.6.363-1.x86_64.rpm
    https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-3.2.9.tgz
    https://downloads.mongodb.com/linux/mongodb-linux-x86_64-enterprise-rhel70-3.2.9.tgz
    https://repo.mongodb.com/yum/redhat/7/mongodb-enterprise/3.2/x86_64/RPMS/mongodb-enterprise-server-3.2.9-1.el7.x86_64.rpm
    https://s3.amazonaws.com/mongodb-training/advadmin/validation/validate_replicasetreconfig.py
    https://s3.amazonaws.com/mongodb-training/advadmin/validation/validate_securedreplicaset.py
    https://s3.amazonaws.com/mongodb-training/advadmin/datasets/usb_drive.zip
)
PACKAGES=(
    unzip
)
# MongoDB enterprise dependencies
# cyrus-sasl cyrus-sasl-plain cyrus-sasl-gssapi krb5-libs 
#            lm_sensors-libs net-snmp-agent-libs net-snmp openssl rpm-libs 
#            tcp_wrappers-libs

### Setup
[ -d $DIR ] || mkdir -p $DIR
cd $DIR
pwd

### Download files
echo Starting to download files
for file in ${FILES[@]}; do
    echo Downloading $file
    curl $file -O
done
echo Done Downloading files

### Packages
for package in ${PACKAGES[@]}; do
    yum install -y $package
done

### Commands to run
# disable SELINUX
/bin/sed -i -e 's/^SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config
echo 0 > /sys/fs/selinux/enforce
# unzip the data file
/bin/unzip usb_drive.zip
# create additional directories, links, ...
mkdir -p /data/etc
chmod 777 /data/etc
rm /share
ln -s /data /share
# stop the already installed mongod on the old AMI
service mongod stop

