Objective
+++++++++

The objective of this exercise is to work through several security concepts in MongoDB.

Premise
+++++++

.. start-premise

*You've discovered a 3 node replica set running without SSL and not utilizing your internal LDAP service for authentication.*

.. end-premise

The goals of this exercise are to convert a running 3 node MongoDB replica set to use SSL for encrypted traffic and LDAP for user authentication.

.. start-setup

1. Connect to your team's instance with the "ubuntu" user for this exercise: ::

    ssh ec2-xx-xxx-xx-xx.compute-1.amazonaws.com
      -l ubuntu –i /path/to/AdvancedOpsTraining.pem


2. Verify the 3 node replica set is running (locally, on ports 27017, 27018, 27019): ::

    /usr/bin/mongo
    > rs.status()

3. Verify the local OpenLDAP server is running: ::

    sudo testsaslauthd -u ldapuser -p ldap

.. end-setup

All certificates needed are in /home/ubuntu/ssl_certs

Now you must determine the steps needed to convert this 3 node replica set to use SSL and LDAP for authentication.  Upon completing the exercise, the following command will return success: ::

    /usr/bin/mongo admin --ssl --sslCAFile ~/ssl_certs/ca.pem
      --sslPEMKeyFile ~/ssl_certs/client.pem --port 27017
    > db.getSiblingDB("$external").auth(
      {
        mechanism: "PLAIN",
        user: "ldapuser",
        pwd:  "ldap",
        digestPassword: false
      })

.. include:: newpage.tmpl


