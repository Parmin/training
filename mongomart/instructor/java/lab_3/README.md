Lab 3 Solution
==============

Please type in solution with the class instead of distributing source code.

The majority of this exercise will be for students to set up a local three node replica set.  The application changes will be minimal.

Modify the MongoClient object in mongomart.py
---------------------------------------------

```
connection = pymongo.MongoClient(connection_string, replicaset='rs0', w='majority')
```




