#!/bin/bash

# Script that downloads and install packages on the instances
# You can test the 'download' part of this test by running it on your Mac.
#   You just need a "/share/downloads" directory being writable

### TODO
# - ability to pull from the files from the 'devel' area
# - ability to download the 'datasets' and 'validation' scripts from a test location
# - test for error codes in running commands and return them to the caller!?

### Machine Role: opsmgr and node

### Files and S3 directories to download
TARGETDIR=/share/downloads
BUCKETFOLDERS=(
    certs,advadmin/certs
    config,advadmin/config
    validation,advadmin/validation
)
FILES=(
    .,https://s3.amazonaws.com/mongodb-training/advadmin/config/README_installation
    .,https://s3.amazonaws.com/mongodb-training/advadmin/datasets/usb_drive.zip
    opsmgr_packages,https://downloads.mongodb.com/on-prem-mms/rpm/mongodb-mms-3.4.3.402-1.x86_64.rpm
    mongodb_packages,https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-3.2.12.tgz
    mongodb_packages,https://downloads.mongodb.com/linux/mongodb-linux-x86_64-enterprise-rhel70-3.2.12.tgz
    mongodb_packages,https://repo.mongodb.com/yum/redhat/7/mongodb-enterprise/3.4/x86_64/RPMS/mongodb-enterprise-3.2.12-1.el7.x86_64.rpm
    mongodb_packages,https://repo.mongodb.com/yum/redhat/7/mongodb-enterprise/3.4/x86_64/RPMS/mongodb-enterprise-server-3.2.12-1.el7.x86_64.rpm
    mongodb_packages,https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-3.4.2.tgz
    mongodb_packages,https://downloads.mongodb.com/linux/mongodb-linux-x86_64-enterprise-rhel70-3.4.2.tgz
    mongodb_packages,https://repo.mongodb.com/yum/redhat/7/mongodb-enterprise/3.4/x86_64/RPMS/mongodb-enterprise-3.4.2-1.el7.x86_64.rpm
    mongodb_packages,https://repo.mongodb.com/yum/redhat/7/mongodb-enterprise/3.4/x86_64/RPMS/mongodb-enterprise-server-3.4.2-1.el7.x86_64.rpm
    apps,https://s3.amazonaws.com/mongodb-training/security_lab/security_lab.tgz
)

## Packages to install with 'yum'
PACKAGES=(
    unzip
    gcc
    gcc-c++
    epel-release
    nodejs

)

# Those are not downloaded, neither installed
# MongoDB enterprise dependencies
# cyrus-sasl cyrus-sasl-plain cyrus-sasl-gssapi krb5-libs
#            lm_sensors-libs net-snmp-agent-libs net-snmp openssl rpm-libs
#            tcp_wrappers-libs

rm /share
ln -s /data /share

### Download dirs and files
[ -d $TARGETDIR ] || mkdir -p $TARGETDIR
cd $TARGETDIR
echo Current Directory:
pwd

echo Starting to download dirs
for line in ${BUCKETFOLDERS[@]}; do
    tgtsrc=(${line//,/ })
    echo Downloading directory ${tgtsrc[1]}
    BUCKETFILES=$(curl mongodb-training.s3.amazonaws.com?prefix=${tgtsrc[1]} | perl -lne 'while(/<Key>(.*?)<\/Key>/g){print("$1\n")}')
    for file in ${BUCKETFILES[@]}; do
        echo Downloading file $file into ${tgtsrc[0]}
        mkdir -p ${tgtsrc[0]}
        chmod 777 ${tgtsrc[0]}
        (cd ${tgtsrc[0]}; curl https://s3.amazonaws.com/mongodb-training/${file} --create-dirs -O)
    done
done
echo Done Downloading dirs

echo Starting to download individual files
for line in ${FILES[@]}; do
    tgtsrc=(${line//,/ })
    echo Downloading file ${tgtsrc[1]} into ${tgtsrc[0]}
    mkdir -p ${tgtsrc[0]}
    chmod 777 ${tgtsrc[0]}
    (cd ${tgtsrc[0]}; curl ${tgtsrc[1]} --create-dirs -O)
done

echo Done Downloading individual files

# This means you are on Mac, the rest won't work, however you probably got your testing.
dist=$(uname)
if [ "$dist" = "Darwin" ]
then
    exit
fi

### Install the packages
for package in ${PACKAGES[@]}; do
    yum install -y $package
done

# unzip the USB drive file
/usr/bin/unzip -o usb_drive.zip

### Commands to run
# disable SELINUX
/bin/sed -i -e 's/^SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config
echo 0 > /sys/fs/selinux/enforce

# create additional directories, links, ...
mkdir -p /share/etc
chmod 777 /share/etc
# create cache dir
mkdir -p /share/cache
chmod 777 /share/cache
# link the certificate directory
ln -s /share/downloads/certs /etc/ssl/mongodb

# copy config files to /share/etc
cp /share/downloads/config/appdb.cnf /share/etc/appdb.conf
cp /share/downloads/config/backupdb.cnf /share/etc/backupdb.conf

# add all the role names and their corresponding IPs to the /etc/hosts file
cat /share/downloads/config/etchosts >> /etc/hosts

# adding write permissions to /var/log/mongodb
chmod 777 -R /var/log/mongodb

# adding datapaths
mkdir -p /mongod-data/{appdb,backupdb}/data

#adding auditing locations
mkdir -p /mongod-data/audit/SECURED/
chmod 777 -R /mongod-data
# some Python modules
pip install simplejson

# change the hostname on the nodeX machines
ip=`hostname --ip-address`

if [ ${#ip} == 10 ]; then
  last_two_ip_num=${ip:8:2}
  node_num=${last_two_ip_num#0}
  node=node$node_num
else
  node_num=${ip:8:1}
  node=opsmgr$node_num
fi

sudo hostnamectl set-hostname $node
sudo echo 'preserve_hostname: true' >> /etc/cloud/cloud.cfg
sudo reboot
