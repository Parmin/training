##!/bin/bash
sudo hostname localhost
sudo sed -i 's/127.0.0.1 localhost/127.0.0.1/' /etc/hosts
sudo apt-get install -y slapd ldap-utils sasl2-bin

# Make sure slapd can start
echo -e "\t" '===================================================='
echo -e "\t  				Starting slapd"
echo -e "\t" '===================================================='
sudo service slapd start

# Add our users
echo -e "\t" '===================================================='
echo -e "\t  				Adding LDAP users"
echo -e "\t" '===================================================='
sudo ldapadd -x -D "cn=admin,dc=mongodb,dc=com" -w password -f users.ldif

# setup saslauthd
echo -e "\t" '===================================================='
echo -e "\t  				Configuring saslauthd"
echo -e "\t" '===================================================='
sudo sed -i 's/START=no/START=yes/' /etc/default/saslauthd
sudo sed -i 's/MECHANISMS="pam"/MECHANISMS="ldap"/' /etc/default/saslauthd
sudo sed -i 's/OPTIONS="-c -m \/var\/run\/saslauthd"/OPTIONS="-m \/var\/run\/saslauthd"/' /etc/default/saslauthd
sudo cat <<'EOF' > /etc/saslauthd
ldap_servers: ldap://localhost:389
ldap_search_base: dc=mongodb,dc=com
ldap_filter: (uid=%u)
EOF

# ensure saslauthd is properly configured
sudo cp /etc/saslauthd /etc/saslauthd.conf
echo -e "\t" '===================================================='
echo -e "\t  				Testing saslauthd"
echo -e "\t" '===================================================='
sudo service saslauthd start
sudo testsaslauthd -u ldapuser -p ldap
