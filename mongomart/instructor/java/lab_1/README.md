Lab 1 Solution
==============

Please type in solution with the class instead of distributing source code.

- Look at the main method of MongoMart.java for the connection
- The constructors of CartDao and ItemDao should have code similar to the following:

```
cartCollection = mongoMartDatabase.getCollection("cart");
```

```
itemCollection = mongoMartDatabase.getCollection("item");
```