Lab 1 Solution
==============

Please type in solution with the class instead of distributing source code.

- Look at the database variable on line 160 of mongomart.py
- Properly initialize the connection the the local instance, and connect to the "mongomart" database

```
connection_string = "mongodb://localhost"
connection = pymongo.MongoClient(connection_string)
database = connection.mongomart
```
