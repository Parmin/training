#!/usr/bin/env bash

sudo service slapd start

sudo ldapadd -Y EXTERNAL -H ldapi:/// -f /vagrant/ldap/pw.ldif
sudo ldapadd -x -D "cn=Manager,dc=mongodb,dc=com" -w password -f /vagrant/ldap/Domain.ldif
sudo ldapadd -x -D "cn=Manager,dc=mongodb,dc=com" -w password -f /vagrant/ldap/Users.ldif
