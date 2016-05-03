set -x

#looks like we need to do some weirdness to get pip...not sure why yum cant find the normal packages
wget http://peak.telecommunity.com/dist/ez_setup.py
python ez_setup.py
easy_install pip

yum -y install openldap-servers openldap-clients openldap-devel python-devel gcc cyrus-sasl-plain xfsprogs net-snmp ps-misc wget 
pip install python-ldap

service slapd stop
service slapd start
#just in case
sleep 10

ldapadd -Y EXTERNAL -H ldapi:/// -f /vagrant/config/ldap/pw.ldif
# Add our specifics
ldapadd -x -D "cn=Manager,dc=10gen,dc=me" -w password -f /vagrant/config/ldap/Domain.ldif
ldapadd -x -D "cn=Manager,dc=10gen,dc=me" -w password -f /vagrant/config/ldap/Users.ldif
# setup saslauthd
sed -i 's/MECH=pam/MECH=ldap/' /etc/sysconfig/saslauthd
cp /vagrant/config/ldap/saslauthd.conf /etc/
service saslauthd start
# Add the users
echo bugs > /vagrant/config/users
echo features >> /vagrant/config/users
echo dbadmin >> /vagrant/config/users
python /vagrant/config/ldap/ldapconfig.py -f /vagrant/config/users

testsaslauthd -u bugs -p password -s mongod -f /var/run/saslauthd/mux
#Show your work!
ldapsearch -x -LLL -b dc=10gen,dc=me
ldapsearch -x -b '' -s base '(objectclass=*)' namingContexts

#Set up mongod.conf
echo "auth=true" >> /home/vagrant/mongod.conf
echo "setParameter=saslauthdPath=/var/run/saslauthd/mux" >> /home/vagrant/mongod.conf
echo "setParameter=authenticationMechanisms=PLAIN" >> /home/vagrant/mongod.conf
