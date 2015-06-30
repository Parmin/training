Lab 1 Solution
==============

It is important to type in these solutions, instead of just showing the students the file.

- Look at the main method of MongoMart.java for the connection
- The constructors of CartDao and ItemDao should have code similar to the following:

```
cartCollection = mongoMartDatabase.getCollection("cart");
```

```
itemCollection = mongoMartDatabase.getCollection("item");
```