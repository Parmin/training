Lab 4 Solution
==============

Create a new ReviewDao class
----------------------------

- Add a review to the "review" collection
- Count the number of reviews for an item
- Find the average number of stars for an item (used to update an "item" document), round it to an integer


Modify the ItemDao.addReview method
-----------------------------------

- Push the latest 10 reviews on to the "reviews" field
- Update the "stars" field for an item (after calculating the average stars for all reviews of an ite)

```
db.item.update( { "_id" : 1 }, { $set: { "stars" : 4.3 }, $push : { "reviews" : {
            $each : [{ "name" : "Name", "date" : ISODate("2016-06-30T23:27:22.163Z"), "comment" : "here", "stars" : 5 } ],
            $sort : { "date" : -1 },
            $slice : 10
         } } })
```

Modify the ItemDao.getItem method
---------------------------------

- No longer dynamically calculate the number fo stars for an item (based on the item's review array)

StoreController
---------------

- Load the number of reviews for an item

item.ftl
--------

- Change "Reviews" to "Latest 10 Reviews"



