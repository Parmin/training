Lab 3 Solution
==============

Please type in solution with the class instead of distributing source code.

The majority of this exercise will be for students to set up a local three node replica set.  The application changes will be minimal.

Modify the connection string in MongoMart.java
----------------------------------------------

```
new MongoMart("mongodb://localhost:27017,localhost:27018,localhost:27019");
```

Modify the CartDao constructor
------------------------------

```
public CartDao(final MongoDatabase mongoMartDatabase) {
        cartCollection = mongoMartDatabase.getCollection("cart").withWriteConcern(WriteConcern.MAJORITY);
    }
```

