#!/bin/sh

# This script will run system requirement checks for the rdbms2mongodb lab

RED='\033[0;31m'
NC='\033[0m'
GREEN='\033[0;32m'

expected_mysqlversion="5.7"
expected_mongodb="v3.4"
expected_java="1.8"
expected_maven="3.5"

SOMETHING_MISSING=0

function print_good {
   printf "${GREEN}$1${NC}\n"
}

function print_error {
  printf "${RED}$1${NC}\n"
  SOMETHING_MISSING=1
}

function check_version {
  version=$( $1 --version|head -1|awk '{ print $3 }'|awk -F\, '{ print $1}'|awk -F\. '{print $1"."$2}' )
  if [ "$version" != "$2" ]
  then
    print_error "Your current version $version is not the expected: $2"
  else
    print_good "Correct version found: $version"
  fi
}

function check_java_version {
  version=$( $1 -version 2>&1|head -1|awk '{ print $3 }'|awk -F\, '{ print $1}'|awk -F\. '{print $1"."$2}'| tr -d '"' )
  if [ "$version" != "$2" ]
  then
    print_error "Your current version $version is not the expected: $2"
  else
    print_good "Correct version found: $version"
  fi
}

function check_mysql {
  echo "Check for MySQL installation and version: $expected_mysqlversion"
  mysqld_exec=$(which mysqld)
  if [ ! -z $mysqld_exec ]
  then
    print_good "MySQL installed: $mysqld_exec"
    check_version $mysqld_exec $expected_mysqlversion
  else
    print_error "mysqld could not be found!"
  fi
}

function check_mongodb {
  echo "Check for MongoDB installation and version: $expected_mongodb"
  mongod_exec=$(which mongod)
  if [ ! -z $mongod_exec ]
  then
    print_good "MongoDB installed: $mongod_exec"
    check_version $mongod_exec $expected_mongodb
  else
    print_error "mongod could not be found!"
  fi
}

function check_java {
  echo "Check for Java installation and version: $expected_java"
  jexec=$(which java)
  if [ ! -z $jexec ]
  then
    print_good "Java installed: $jexec"
    check_java_version $jexec $expected_java
  else
    print_error "java could not be found!"
  fi
}

function check_maven {
  echo "Check for Maven installation and version: $expected_maven"
  m_exec=$(which mvn)
  if [ ! -z $m_exec ]
  then
    print_good "Maven installed: $m_exec"
    check_version $m_exec $expected_maven
  else
    print_error "mvn could not be found!"
  fi
}

check_mongodb
check_mysql
check_java
check_maven

if [ $SOMETHING_MISSING != 0 ]
then
  print_error "Check your setup! Something seems to be missing."
fi

exit $SOMETHING_MISSING
