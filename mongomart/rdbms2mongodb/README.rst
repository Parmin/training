Welcome to MongoMart RDBMS
==========================

This version is supported by a MySQL database.

For this workshop we assume that you have previously installed the following
pre-requisites:

- mysql server
- mysql client
- java
- maven

To get started we first need to do the following set of steps:

1- Launch MySQL Server
----------------------

Make sure you MySQL server and shell client to interact with the database.

.. code-block:: sh

  mysql.server start

2 - Import rdbms Schema
-----------------------

.. code-block:: sh

  mysql -uroot < dataset/create_schema.sql

3 - Import mysqldump
--------------------

.. code-block:: sh

  mysql -uroot < dataset/dump/mongomart.sql
  mysql -uroot < dataset/check.sql

4 - Build Package
-----------------

.. code-block:: sh

  mvn package -f java/pom.xml


5 - Run Package
---------------

.. code-block:: sh

  java -jar java/target/MongoMart-1.0-SNAPSHOT.jar

Apply Our Solution
------------------

In order to ensure that you moving smoothly through the exercises, 
you can apply our pre-built solutions to the exercises/labs that you 
are working on.

.. code-block:: sh

  ./solvethis.sh lab1

Running this script will implement our version of the solution on your machine.
