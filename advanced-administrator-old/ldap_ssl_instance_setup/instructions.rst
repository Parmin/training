The goals of this exercise are to convert a running 3 node MongoDB cluster to use SSL for encrypted traffic and LDAP for user authentication

First, verify the 3 node replica set is running (locally, on ports 27017, 27018, 27019):

/usr/bin/mongo

Second, verify the local OpenLDAP server is running:

sudo testsaslauthd -u ldapuser -p ldap

All certifications needed are in /home/ubuntu/ssl_certs

Now you must determine the steps needed to convert this 3 node replica set to use SSL and LDAP for authentication.  Upon completing the exercise, the following command will work:

/usr/bin/mongo admin --ssl --sslCAFile ~/ssl_certs/ca.pem --sslPEMKeyFile ~/ssl_certs/client.pem --port 27017
> db.getSiblingDB("$external").auth(
   {
     mechanism: "PLAIN",
     user: "ldapuser",
     pwd:  "ldap",
     digestPassword: false
   }
)


Solution:

this needs to happen: sudo chmod 755 /var/run/saslauthd

1. Upgrade cluster to use SSL

Tutorial here may help: http://docs.mongodb.org/manual/tutorial/upgrade-cluster-to-ssl/

Look in /home/ubuntu/ssl_certs:

ca.pem  client.pem  crl.pem  server.pem

First, rolling restart of each node with the following parameters:

sslMode = allowSSL
sslPEMKeyFile = /home/ubuntu/ssl_certs/server.pem
sslCAFile = /home/ubuntu/ssl_certs/ca.pem

Second, either update each config file again, or run the following command on each:

db.getSiblingDB('admin').runCommand( { setParameter: 1, sslMode: "preferSSL" } )

sslMode = preferSSL
sslPEMKeyFile = /home/ubuntu/ssl_certs/server.pem
sslCAFile = /home/ubuntu/ssl_certs/ca.pem

Third, either update each config file again, or run the following command on each:

db.getSiblingDB('admin').runCommand( { setParameter: 1, sslMode: "requireSSL" } )

sslMode = requireSSL
sslPEMKeyFile = /home/ubuntu/ssl_certs/server.pem
sslCAFile = /home/ubuntu/ssl_certs/ca.pem

Checkpoint, to verify SSL is running correctly, connect to each node:

/usr/bin/mongo --ssl --sslCAFile ~/ssl_certs/ca.pem --sslPEMKeyFile ~/ssl_certs/client.pem --port 27017
/usr/bin/mongo --ssl --sslCAFile ~/ssl_certs/ca.pem --sslPEMKeyFile ~/ssl_certs/client.pem --port 27018
/usr/bin/mongo --ssl --sslCAFile ~/ssl_certs/ca.pem --sslPEMKeyFile ~/ssl_certs/client.pem --port 27019

2. LDAP

http://docs.mongodb.org/manual/tutorial/configure-ldap-sasl-openldap/

- Create admin user

> use admin
> db.createUser(
    {
      user: "superuser",
      pwd: "mongo",
      roles: [ "root" ]
    }
)

Add a keyfile and enable authentication for the cluster:

> openssl rand -base64 741 > mongodb-keyfile
auth=true
setParameter=saslauthdPath=/var/run/saslauthd/mux
setParameter=authenticationMechanisms=PLAIN,MONGODB-CR
keyFile=/home/ubuntu/mongodb-keyfile

Note: auth=true is not needed when a keyFile is specified, also combination of PLAIN/MONGODB-CR can be modified

Restart all the nodes

Authenticate with superuser

/usr/bin/mongo admin --ssl --sslCAFile ~/ssl_certs/ca.pem --sslPEMKeyFile ~/ssl_certs/client.pem --port 27017 -u superuser -p mongo

Add ldap user

db.getSiblingDB("$external").createUser(
    {
      user : "ldapuser",
      roles: [ { role: "read", db: "records" } ]
    }
)

Log back in with new ldap user ro verify:

/usr/bin/mongo admin --ssl --sslCAFile ~/ssl_certs/ca.pem --sslPEMKeyFile ~/ssl_certs/client.pem --port 27017

> db.getSiblingDB("$external").auth(
   {
     mechanism: "PLAIN",
     user: "ldapuser",
     pwd:  "ldap",
     digestPassword: false
   }
)
