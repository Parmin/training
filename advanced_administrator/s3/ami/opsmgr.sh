#!/bin/bash

### TODO
# - ability to download the 'datasets' and 'validation' scripts from a test location
# - test for error codes in running commands and return them to the caller!?

### Machine Role: opsmgr and node

### Files to download
DIR=/data/downloads
FILES=(
    https://downloads.mongodb.com/on-prem-mms/rpm/mongodb-mms-3.4.3.402-1.x86_64.rpm
    https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-3.4.2.tgz
    https://downloads.mongodb.com/linux/mongodb-linux-x86_64-enterprise-rhel70-3.4.2.tgz
    https://repo.mongodb.com/yum/redhat/7/mongodb-enterprise/3.4/x86_64/RPMS/mongodb-enterprise-server-3.4.2-1.el7.x86_64.rpm
    https://s3.amazonaws.com/mongodb-training/advadmin/config/appdb.cnf
    https://s3.amazonaws.com/mongodb-training/advadmin/config/backupdb.cnf
    https://s3.amazonaws.com/mongodb-training/advadmin/config/etchosts
    https://s3.amazonaws.com/mongodb-training/advadmin/validation/validate_replicasetreconfig.py
    https://s3.amazonaws.com/mongodb-training/advadmin/validation/validate_securedreplicaset.py
    https://s3.amazonaws.com/mongodb-training/advadmin/datasets/usb_drive.zip
    https://s3.amazonaws.com/mongodb-training/security_lab/security_lab.tgz
)
PACKAGES=(
    unzip
    gcc 
    gcc-c++
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
# create cache dir
mkdir -p /data/cache
chmod 777 /data/cache
rm /share
ln -s /data /share
# stop the already installed mongod on the old AMI
service mongod stop

# move config files to /share/etc
cp /share/downloads/appdb.cnf /share/etc/appdb.conf
cp /share/downloads/backupdb.cnf /share/etc/backupdb.conf

# add all the role names and their corresponding IPs to the /etc/hosts file
cat /share/downloads/etchosts >> /etc/hosts

# adding write permissions to /var/log/mongodb
chmod 777 -R /var/log/mongodb

# adding datapaths
mkdir -p /mongod-data/{appdb,backupdb}/data
chmod 777 -R /mongod-data
