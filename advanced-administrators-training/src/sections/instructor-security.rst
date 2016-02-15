Premise 1
+++++++++

.. include:: student-security.rst
   :start-after: start-premise
   :end-before: end-premise

Setup
+++++

- Start new instances specifically for this exercise with the securityRepl.sh script, e.g. "./security.sh 2 jason" for two teams for the instructor "jason"

Solution SSL
++++++++++++

1. Tutorial here may help: http://docs.mongodb.org/manual/tutorial/upgrade-cluster-to-ssl/

2. Look in /home/ubuntu/ssl_certs: ::

    ca.pem  
    client.pem  
    crl.pem  
    server.pem

3. Rolling restart of each node with the following parameters: ::

    sslMode = allowSSL
    sslPEMKeyFile = /home/ubuntu/ssl_certs/server.pem
    sslCAFile = /home/ubuntu/ssl_certs/ca.pem

4. Either update each config file again, or run the following command on each: ::

    db.getSiblingDB('admin').runCommand( { setParameter: 1, sslMode: "preferSSL" } )

    // Or config file changes
    sslMode = preferSSL
    sslPEMKeyFile = /home/ubuntu/ssl_certs/server.pem
    sslCAFile = /home/ubuntu/ssl_certs/ca.pem

5. Update each config file again, or run the following command on each: ::
 
    db.getSiblingDB('admin').runCommand( { setParameter: 1, sslMode: "requireSSL" } )

    sslMode = requireSSL
    sslPEMKeyFile = /home/ubuntu/ssl_certs/server.pem
    sslCAFile = /home/ubuntu/ssl_certs/ca.pem

6. Checkpoint, to verify SSL is running correctly, connect to each node: ::

    /usr/bin/mongo --ssl --sslCAFile ~/ssl_certs/ca.pem 
        --sslPEMKeyFile ~/ssl_certs/client.pem --port 27017
    /usr/bin/mongo --ssl --sslCAFile ~/ssl_certs/ca.pem 
        --sslPEMKeyFile ~/ssl_certs/client.pem --port 27018
    /usr/bin/mongo --ssl --sslCAFile ~/ssl_certs/ca.pem 
        --sslPEMKeyFile ~/ssl_certs/client.pem --port 27019


Solution LDAP
+++++++++++++

1. Tutorial here may help: http://docs.mongodb.org/manual/tutorial/configure-ldap-sasl-openldap/

2. Create admin user (we'll use this user to add our LDAP user): ::

    > use admin
    > db.createUser(
        {
          user: "superuser",
          pwd: "mongo",
          roles: [ "root" ]
        }
    )

3. Add a keyfile and enable authentication for the cluster: ::

    > openssl rand -base64 741 > mongodb-keyfile

    // Modify config files
    auth=true
    setParameter=saslauthdPath=/var/run/saslauthd/mux
    setParameter=authenticationMechanisms=PLAIN,MONGODB-CR
    keyFile=/home/ubuntu/mongodb-keyfile

    Note: auth=true is not needed when a keyFile is specified, 
    also combination of PLAIN/MONGODB-CR can be modified

4. Restart all the nodes

5. Authenticate with superuser: ::

    /usr/bin/mongo admin --ssl --sslCAFile ~/ssl_certs/ca.pem 
        --sslPEMKeyFile ~/ssl_certs/client.pem --port 27017 -u superuser -p mongo

6. Add ldap user: ::

    db.getSiblingDB("$external").createUser(
        {
          user : "ldapuser",
          roles: [ { role: "read", db: "records" } ]
        }
    )

7. Log back in with new ldap user ro verify: ::

    /usr/bin/mongo admin --ssl --sslCAFile ~/ssl_certs/ca.pem 
        --sslPEMKeyFile ~/ssl_certs/client.pem --port 27017

    > db.getSiblingDB("$external").auth(
       {
         mechanism: "PLAIN",
         user: "ldapuser",
         pwd:  "ldap",
         digestPassword: false
       }
    )
