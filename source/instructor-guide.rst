================================
MongoDB University: Fundamentals
================================


Materials
---------
- One workbook per student
- Provided swag (bag, shirts, pens, etc)
- One computer per student, ideally with MongoDB pre-installed
- Notepads for students to write on during group activities
- A projector and screen
- A whiteboard
- Instructor materials for delivering the course


Best Practices when Leading Training Sessions
---------------------------------------------
- Breaks: Call 10-minute breaks every 90 minutes at least. 
- Make extensive use of the white board. Please avoid using slides. 
- Write down key concepts. Students who both see and hear something are more likely to pick it up than students who just hear it.
- Start on time and end on time. 
- If you have a suggested improvement or other comment, please email training@mongodb.com.


MongoDB Overview
----------------

.. topic:: Learning objectives 

   Students should understand:

   - The advantages of MongoDB over relational databases 
   - The advantages of MongoDB over a key/value store.
   - The difference between vertical and horizontal scaling
   - The advantages of horizontal scaling
   - The role of MongoDB in the development stack

MongoDB is a document database. Documents are associative arrays like:

- Python dictionaries
- Ruby hashes 
- PHP arrays
- JSON objects

Where relational databases store rows, MongoDB stores documents.

::

   {
       "a" : 3,
       "b" : [3, 2, 7], 
       "c" : { 
           "d" : 4 , 
           "e" : "asdf",
           "f" : true
       }
   }   

This is a fundamental departure from relational where rows are flat; documents are hierarchical data structures.

Another difference is in terms of scalability. With an RDBMS:

- If you need to support a larger workload, you buy bigger machine. 
- The problem is, machines are not priced linearly. 
- The largest machines cost much more than commodity hardware. 
- If you're successful, you'll find you simply can't buy a large enough a machine to support your workload. 

.. figure:: ./figures/figure_scaling_up.jpg
    :width: 400px
    

With MongoDB:

- MongoDB is designed to be horizontally scalable through sharding by simply adding boxes. 
- When you need more performance, you just buy another machine and add it to your cluster. 
- MongoDB is highly performant on commodity hardware.	

.. figure:: ./figures/figure_scaling_out1.png
    :width: 400px


How does MongoDB achieve horizontal scalability? Let's take a look at the database landscape.

- We'll plot each technology in terms of scalability and depth of functionality. 
- At the top left, we have key value stores like memcached. These scale very well, but are lacking features that make developers productive. 
- At the far right we have traditional RDBMS technologies like Oracle and MySQL. These are full featured, but will not scale easily. 

.. figure:: ./figures/figure_database_landscape.png
    :width: 400px


Why don't RDBMS technologies scale?

- Two reasons: joins and transactions. 
- These are difficult to run in parallel.


MongoDB sits at the knee of the curve:

- It has nearly as much scalability as key value stores.
- Gives up only the features that prevent scaling. 
- And we have compensating features that mitigate the impact of that design decision.

.. figure:: ./figures/deployment_models.jpg
    :width: 400px

MongoDB supports high availability:

- We're talking about automated failover. 
- Typical deployments use replica sets of 3 or more nodes.
- The primary node will accept all writes, and possibly all reads. 
- Each secondary will read from the oplog (operations log) of another node to keep itself up to date
- If your primary goes down, the secondaries will automatically hold an election for a new primary. This usually takes just a few seconds.
- Replica sets provide redundancy and high availability for your data.
- Replication is not MongoDBs scaling solution. 
- MongoDB scales using sharding.


In production, you typically build a fully sharded cluster:

- Your data is distributed across several shards.
- The shards are themselves replica sets. 
- This provides high availability and redundancy at scale.

MongoDB Stores Documents
------------------------

.. topic:: Learning objectives 

   Students should understand:

   - JSON syntax
   - The structure of documents in MongoDB
   - Array fields
   - Embedded documents
   - Deeper nested structures
   - BSON data types
   - BSON structure
   - Padding factor*
   - Power of two sizing*


JSON:

- JavaScript Object Notation
- Objects are associative arrays.
- They are composed of name/value pairs.
- Example:
  ::
      { 
          "firstname" : "Thomas",
          "lastname" : "Smith",
          "age" : 29
      }


JSON field names and values:

- Field names must be strings (use double quotes).
- Values may be any of the following:

  - string (e.g., "Thomas")
  - number (e.g., 29, 3.7)
  - true / false
  - null
  - array (e.g., [88.5, 91.3, 67.1])
  - object (See above.)

- The elements of an array may be any of the values specified above.
- More example objects:
  ::
      {
          "first key" : "value" , 
          "second key : {
              "first nested key" : "first nested value", 
              "second nested key" : "second nested value"
	   }, 
	   "third_key" : [ 
	       "first array element", 
               "second element",
               { "nested key" : "nested value" } , 
               [ "nested array element 1", "nested array element 2"] 
           ]
      }

- More detail at json.org_.

.. _json.org: http://json.org/


BSON:

- MongoDB stores documents in a format known as "Binary JSON" or BSON.
- The MongoDB drivers (client libraries) also send and receive data in this format.
- However, within your application you work with native mappable data structures such as dictionaries. 
- The drivers abstract away the fact that they communicate with the server using BSON. 
- BSON provides support for all JSON data types and several others. They are as follows:

  - ISODate
  - Int32
  - Int64
  - Double
  - ObjectId
  - Binary
- See bsonspec.org_.

.. _bsonspec.org: http://bsonspec.org/#/specification


BSON hello world:

::

    JSON:
        { "hello" : "world" }

    BSON:
        "\x16\x00\x00\x00\x02hello\x00 
         \x06\x00\x00\x00world\x00\x00"

- \\x16\\x00\\x00\\x00 (document size) 
- \\x02 = string (data type of field value)
- hello\\x00 (key/field name, \\x00 is null and delimits the end of the name)
- \\x06\\x00\\x00\\x00 (size of field value including end null)
- world\\x00 (field value) 
- \\x00 (end of the document)


A more complex BSON example:

::

    JSON:
        { "favoriteThings" : [ "awesome", 5.05, 1986 ] }

    BSON:
        "\x3b\x00\x00\x00\x04BSON\x00\x26\x00 
         \x00\x00\x020\x00\x08\x00\x00 
         \x00awesome\x00\x011\x00\x33\x33\x33\x33\x33\x33 
         \x14\x40\x102\x00\xc2\x07\x00\x00 
         \x00\x00"


Documents, Collections, and Databases:

- Documents are stored in collections.
- Collections are contained in a database. 
- Example:
  - Database: products
  - Collections: books, movies, music
- Each database-collection combination defines a namespace, e.g.:
  - products.books 
  - products.movies
  - products.music

The _id field:

- All documents must have an _id field.
- The _id is immutable.
- If no _id is specified when a document is inserted, MongoDB will add the _id field and assign a unique ObjectId for the document before inserting.
- Most drivers will actually create the ObjectId if no _id is specified.
- The _id field is unique to a collection (namespace).

.. figure:: ./figures/figure_id_values.jpg
    :width: 400px


How ObjectIds are created:
- An ObjectId is a 12-byte value. 
- The first 4 bytes will be a datetime reflecting when the ObjectID was created. 
- The next 3 bytes will be a MAC address.
- Then a 2-byte process ID
- And, finally, 3 bytes that are monotonically increasing for each new ObjectId created within a collection. 


Storing BSON documents:

- Each document may be a different size from the others.
- Documents are physically adjacent to each other on disk and in memory.
- If a document is updated such that it will require more bytes on disk, MongoDB may have to move the document. 
- This may cause fragmentation, resulting in unnecessary I/O.  
- MongoDB has strategies to reduce the effects of document growth:
  - Padding factor
  - usePowerOf2Sizes


Padding Factor:  

- MongoDB will "pad" a document with extra bytes if documents in a collection have been observed to grow.  
- The "padding factor" is a multiplier that defaults to 1 (no padding).
- As documents in a collection grow and need to be moved, MongoDB will begin to add padding.
- At a padding factor of 2, the document will be inserted at twice its actual size
- With padding documents will not be as likely to move after update operations providing room to grow into.  
- This setting is not tunable it is updated automatically.

::

  TODO: Insert a figure the illustrates padding factor.


usePowerOf2Sizes:

- When a document must move to a new location this leaves a fragment.  - MongoDB will attempt to fill this fragment with a new document eventually.  
- As of MongoDB 2.6, collections have a setting called "usePowerOf2Sizes" enabled by default.  
- This setting will round the size of the document up to the next power of 2. 
- For example, a document that 118 bytes will be allocated 128 bytes. - Power of two sizes make it easier for MongoDB to find new document to fill fragmented space. 
- This results in less overall fragmentation.  
- This is analogous to a building a wall from stone vs. brick.  If a stone crumbled it would prove difficult to find a new stone to fill the space. Replacing a brick, however, is easy.
- Power of two sizing was introduced in MongoDB 2.4, but must be enabled using the colMod operation.  
- If a collection is read only, users should disable usePowerof2Sizes in MongoDB 2.6 and above. 

::

  TODO: Insert a figure the illustrates usePowerOf2Sizes





And now, let's go back to the mongoDB shell. It's time to learn CRUD.


CRUD
Objective: Students get familiarized with the basic operations of an app in MongoDB and how data is read/modified, as well as how to interact with the shell.

DRAW:
	C	R	U	D
	R	E	P	E
	E	A	D	L
	A	D	A	E
	T		T	T
	E		E	E


Let's all bring up the MongoDB shell now.

We're going to learn about CRUD at this point, or Create, Read, Update, and Delete; the basic set of operations for manipulating and querying data in any database. For MongoDB, we will use the following commands when we are manipulating things at the document level:
CREATE: db.collection.insert()
READ: db.collection.find()
UPDATE: db.collection.update()
DELETE: db.collection.remove()

There are a few variants of some of these, but this is the basic set of operations you want to deal with.

This section is full of exercises. Make sure that people are doing them, walk about and verify that it's going correctly. If not, stop and have a little mini-lesson about what they might be doing wrong. Encourage each to help their neighbor. Split up the fast learners, if possible, so that they are sitting next to the slower learners, and can assist them.

Create
Objectives: Students will be able to insert documents into a database.

EXERCISES:
Let's go to a new database. Type the following:
‘use sample'
Now, let's insert the following documents into foo collection (will create a new collection with the first insert if the collection doesn't exist ):
{}
{ a : 1}
{ a : false} 
{ a : 1, b : true }
{ b : -56.5 }
Type ‘db.foo.count()' or count them up after ‘db.foo.find()'. What is your document count? (Pick a student and ask them)
ANSWER: 5
Ask the class if anybody got anything different, and go around and look at terminals. If anyone has problems, NOW is the time to find out!!
Type ‘db.foo.find()'. What field, that you didn't input, is present in every document?
ANSWER: _id


One thing to notice is that the _id, when automatically inserted, is always an ObjectId. However, the _id does NOT have to be an ObjectId. It can be just about anything, except an array, though it can be an embedded document that contains arrays.



EXERCISES
Let's drop the collection:
‘db.foo.drop()'
QUESTION:
How many documents are in the collection now? Type ‘db.foo.find()'
ANSWER: 
0
Now, insert the following documents:
{ a : 1 , _id : 1}
{ _id : true } 
{ b : 1 , _id : "_id" }
{ _id : true, a: 1 }
QUESTION:
What happened with that last insert? Why?
ANSWER: 
Duplicate Key Error. We tried to insert with _id : true 2 times.
SAY: 
"This happened because the _id is made with a Unique Index, so the machine will not allow you to insert two documents with the same _id."
QUESTION:
How many documents are in the collection now? Type ‘db.foo.find()'
ANSWER: 3
Now, let's insert two documents:
db.foo.insert( { _id : new ObjectId() } ) 
db.foo.insert( { _id : new ObjectId().valueOf() } ) 
QUESTION:
What is the difference between these two documents?
ANSWER: One has an _id of type ObjectId, the other has an _id of type string.

You can also use the javascript shell to execute commands. For instance:

SHOW
db.foo.drop()
db.foo.find()
Note that it's empty
for (i=1; i<=50; i++) { db.foo.insert( { _id : i , a : 2 * i + 1 } ) }
db.foo.count()
Show them that it's 50.
db.foo.find()
Show them what it looks like. Ask if they see anything unusual. You're looking for the fact that you've only got the first 20 documents. Jumping ahead to the "READ" section, you can tell them that technically, the find() method returns a pointer to the result set, and the javascript shell iterates automatically over the first 20 (if you don't set the the results to a variable).
it
it
it
Show them that you've got more.

One thing to notice is that the documents appear, in the database, in the order in which they were inserted. Assuming you never modify or delete a document, this will remain the case. They're also written to disk in this order, with the caveat that most databases have multiple files, so there are breaks between files. 

Also, if you delete a document, this will create a hole in the data file, and Mongodb will try to fill that hole on the next insert that is smaller than the hole, but it will probably be a bit fragmented from then on. Also, if an update ends up making a document larger, and it no longer fits in its slot, it will be moved to somewhere it does fit. So deletes and updates can result in some fragmentation of your data and rearranging of your order. I'm going to demonstrate this so you can see it.


Read
Objectives: Students will be able to query the database for information without modifying it, using db.collection.find(), its operators, and its children methods. 

Inserts were pretty straightforward. I just give the database my document, and it puts that document into the collection. 

Reads use find() instead of insert(), and can also be quite simple. However, since people might need to be very specific about what type of document they need, reads 

So far, we've been doing queries (that is, using find() ) with no parameters, which returns a cursor to the entire collection. In the drivers, you will literally get back the cursor, a pointer to your documents. You can invoke this behavior in the shell as well, by the way:

SHOW:
> var x = db.foo.find();

And then you can use the .next() function to iterate on it.

SHOW: 
> if (x.hasNext()) x.next();
> if (x.hasNext()) x.next();
> if (x.hasNext()) x.next();

But the shell will automatically iterate 20 times if you just ask it to display the cursor.

SHOW:
> x

So the find() command returns a cursor to the entire collection, which you can use to get the data set. What is a cursor? It's a pointer to the result set of the quer. 

SHOW
> var x = db.zips.find();
if (x.hasNext()) x.next();
We see a document
if (x.hasNext()) x.next();
Another document
x.hasNext()
true

By the way, if you haven't noticed already, you can use <tab> to autocomplete methods in the MongoDB shell.

SHOW
x.<tab><tab>
So many methods!

This is a good way to explore the javascript shell, and learn object methods. Some of those listed here may not work, because cursors have some methods that they only allow before the first .next() call (such as .sort(); you can't sort after you start pulling documents from the cursor).


Up until this point, we've pretty much been calling find() without parameters. If we want to call find() with a parameter, that parameter will have to be a JSON document (or something analogous, depending on the driver), and it will give us all of the documents that match only those criteria specified in the document. 

SHOW
db.foo.drop()
db.foo.find()
Show them that it's empty
for (i=1; i<=50; i++) { db.foo.insert( { a : i } ) }
db.foo.count()
Show them that it's 50.
for (i=1; i<=50; i++) { db.foo.insert( { a : i } ) }
for (i=1; i<=50; i++) { db.foo.insert( { a : i } ) }
for (i=1; i<=50; i++) { db.foo.insert( { a : i } ) }
db.foo.count()
Should be 200.
db.foo.find()
Just the first 20 from the first insert
db.foo.find( { a : 13 } ) 
Gives us all 4 docs with ‘a : 13'.

What we did just there was pass the document { a : 13 } to the find() command. You'll notice that although no documents in the database are precisely { a : 13 } (since all of them have _id's), we got some documents back. So the first argument of a find() query will return all documents with a key:value pair listed. 


Now, let's do something a little more complicated.

SHOW
db.foo.drop()
db.foo.find()
Show them that it's empty
 for( i = 1 ; i <= 10 ; i++ ) { for( j = 1; j <= 10 ; j++ ) { for( k = 1 ; k <= 10 ; k++ ) { db.foo.insert( { a : i , b : j , c : k } ) } } }
db.foo.find()
Show them that there are lots of docs

If you use multiple fields in your find() query, then any documents that are returned will match BOTH fields:

SHOW:
db.foo.find( { a : 3 , b : 7 } )
see 10 docs where a is 3 and b is 7.
db.foo.find( { a : 3 , b : 7 } ).count( )
10

But it wouldn't be that useful if you could only get values one at a time. You can get documents with multiple possible values using the $in operator:

db.foo.find( { a: 3, b: {$in: [ 3,  9] } } ).count()
20, all with a:3 and either b: 3 or b: 9

If you want a range of values, you can use the $lt or the $gt operator:

db.foo.find( { a: 3, b: {$lt: 4} } ) .count()
30, all with a:3 b < 4
db.foo.find( { a: { $gt : 8 } , b: {$lt: 4} } ) .count()
60
db.foo.find( { a : 7 , b : { $gt : 3 , $lt : 6 } } ).count()
20, for a: 7 and b: 4 or b: 5


At this point, let's stop making our own data, and start working with some real-world data. We'll go to the tweets collection we imported earlier.

SHOW
use sample
db.tweets.findOne()

This is actual data from Twitter's api. They don't use mongodb, but they do release their tweets publicly, in JSON format, so we can use them. Mongodb assigns an _id when we insert the data, but everything else you see here comes from Twitter.  You can see the structure of the JSON, with subdocuments such as "entities" and "user", and arrays as values. The twitter id is there in the "id" field you can see in the document (not the _id field that MongoDB assigns on insert).

Next thing we're going to look at is a projection.


SHOW
db.zips.findOne()
Has city, zip code, a location, a population, and a state.
Should distinguish between findOne which returns an object and find which returns a cursor (even if it's just one document). 
db.zips.count()
29,470 zip codes in the US
db.zips.find( { }, {city: 1, state: 1, zip: 1}) 


OK, so this is the first time I've given the find() query two parameters. The first parameter is a prototype document for matching the documents in the collection. As I said before, any documents that match the key: value pairs in this prototype document will be in the result set. 

The second parameter is a projection parameter. It's optional, and if you don't specify it, you get the entire document back, however, if you do specify it, then you'll get only those fields that you specify.

There is an exception, however. For the _id field, you need to explicitly state that it should not be shown if you don't want it. So this is why the above query, we got back the _id field in addition to the city/state/zip that we asked for.

This can be used when only a few fields are of interest to you, and it also means that less data needs to be transmitted over the wire when bandwidth is an issue.



SHOW:
db.zips.find( {pop: {$lt: 10} , $or : [{ state: "CA" } , { state : "NY" } ]} )
This will give you the documents with state: (CA or NY) and the population under 10. It illustrates the $or operator, as well as $lt

Now, sometimes you want to reach inside of a subdocument, using what we call "dot notation".

SHOW
db.test3.insert( { x : { y : 10 , z : 15 } } )
db.test3.insert( { x : { y : 20 , z : 15 } } )
db.test3.insert( { x : { y : 2340 , z : 1325 } } )
db.test3.insert( { x : { w : 232, y : 2340 , z : 1325 } } )
db.test3.find( { "x.w" : 232 } ) 
Found it!
db.test3.find( { "x.z" : 15 } )
Found 2!
db.test3.insert( { x : { w : { a : 5 , b : 6 } , y : 2340, z : 1325 } } )
db.test3.find( { "x.w.a" : 5 } ) 
Found one!
db.test3.find( { "x.w.a" : 10 } ) 
Nothing
db.test3.find( { x : { y : 10 , z : 15 } } )
Returns 1
db.test4.insert( { list : [ "matt" , "oz" , "jay" ] } )
db.test4.insert( { list : [ "will" , "oz" , "dave" ] } )
db.test4.insert( { list : [ "mike" ] } )
db.test4.find( { list : "mike" } ) 
1 hit
db.test4.find( { list : "oz" } )
2 hits
db.test4.find( { list : [ "oz" ] } ) 
No hits, because you need to match the entire array exactly.

Update
Objectives: Students will be able to replace and update data using the db.collection.update() method, and its various flags/arguments, including multi.

This is handled with ‘db.collection_name.update()'. An update takes a minimum of two arguments: the first is a document to specify which document (or documents) to update, and the second is a document to specify what to change. By default, update() will only update one document, and it will replace that document by the document you put in the second argument's slot.


SHOW
for (i=1; i<=100; i++) db.temp.insert( { a : i } )
db.temp.find( { a : 10 } )
db.temp.update( { a : 10 } , { b : 20 } )
db.temp.find( { b : 20 } )
Hey, the a : 10 is gone!

So, like I said, by default we're going to be replacing a document. 

This is almost never the right way to use mongoDB, but it makes a certain intuitive sense. Find something that matches this first document, and then replace it (while keeping the _id because that is immutable) with this second document.

However, if we only want to change a part of the document, we do have options. 

For example, 

db.temp.find( { b : 22 } ) 
db.temp.update( { a : 11 } , { $set : { b : 22 } } )
db.temp.find( { b : 22 } ) 
It didn't overwrite a : 10 or the _id!


db.temp.update( { _id : 124} , { $set : { foo : "bar"} } ) 
db.temp.find( { _id : 124} )
Couldn't find it!
b.temp.update( { _id : 124} , { $set : { foo : "bar"} } , { upsert : true } )
db.temp.find( { _id : 124} )
Inserted it.
db.temp.update( { } , { $set : { foo : "cat" } } , { multi : true } )
db.temp.find()
Everything was updated!!

If multi: true is not in place, it is false by default, and only the FIRST document found will get updated


Now is probably a good time to talk a little bit about natural order. I mentioned earlier that if you just insert, but don't update or delete, then the order of the documents on disk is the same as the order in which you inserted them, if you allow for fragmentation of the data files.

When documents are only inserted, never updated or deleted, this is the order they go in.
If a document is deleted, but none are inserted/updated, the order will remain the same.
Some updates will grow a document. If the document outgrows its space, it will move to another location, either to the end of the collection, or to a hole.

New documents that are inserted may fill ‘holes' created by deleted or moved documents. 
Later, when we talk about indexes, you should realize that the _id is indexed, so its 
location can be found with the _id. 

We'll talk about indexes more, later. For now, I'm going to have you guys do some exercises.

EXERCISES:  
Using the training.scores namespace, set the proper grade attributes. For example, users with scores greater than 90 get an A. Set the grade to B for scores from 80-89, C for 70-79, D for 60-69, and F for anything below 60.
ANSWER:
Mongodb 2.4+
db.scores.update( { score: { $gte : 90 } } , { $set: {grade : ‘A' } } , { multi : true } }
db.scores.update( { score: { $gte : 80 , $lt : 90 } } , { $set: {grade : ‘B' } } , { multi : true } }
db.scores.update( { score: { $gte : 70 , $lt : 80 } } , { $set: {grade : ‘C' } } , { multi : true } }
db.scores.update( { score: { $gte : 60 , $lt : 70 } } , { $set: {grade : ‘D' } } , { multi : true } }
db.scores.update( { score: { $lt : 60 } } , { $set: {grade : ‘F' } } , { multi : true } }
Mongodb 2.2
db.scores.update( { score: { $gte : } } , { $set: {grade : ‘A' } } , false, true }
To verify: 
> db.scores.aggregate( { $group : { _id : "$grade" , min_score : { $min : "$score" } , max_score : { $max : "$score" } } } )[ "result" ]
Should look something like this: (MongoDB 2.4)
[
	{
		"_id" : "F",
		"min_score" : 1,
		"max_score" : 59
	},
	{
		"_id" : "D",
		"min_score" : 60,
		"max_score" : 69
	},
	{
		"_id" : "C",
		"min_score" : 70,
		"max_score" : 79
	},
	{
		"_id" : "B",
		"min_score" : 80,
		"max_score" : 89
	},
	{
		"_id" : "A",
		"min_score" : 90,
		"max_score" : 100
	}
]
Or, (2.6)
{ "_id" : "F", "min_score" : 1, "max_score" : 59 }
{ "_id" : "D", "min_score" : 60, "max_score" : 69 }
{ "_id" : "C", "min_score" : 70, "max_score" : 79 }
{ "_id" : "B", "min_score" : 80, "max_score" : 89 }
{ "_id" : "A", "min_score" : 90, "max_score" : 100 }
You're being nice, so you decide to add 10 points to every score on every exam whose score is < 60. How do you do this update?
ANSWER: 
First, to see the state of the collection beforehand:
> db.scores.count( { score : {$lt : 60 } } ) 
See how many scores we're going to edit
> db.scores.count( { score : {$lt : 60 , $gte : 50 } } )
See how many scores will be pushed up to D
> db.scores.count({ score : {$gte : 60 , $lt : 70 } } )
This is how many D's there were before.
> db.scores.count( { score : {$lt : 10 } } ) 
Good reference
> db.scores.update( { score : { $lt : 60 } } , { $inc : { score : 10 } } , { multi : true } ) 
TO VERIFY: 
> db.scores.count( { score : {$lt : 60 } } ) 
Should be less than our previous amount by ~10% of sample; difference should be same as the query above that were in the range (50 , 60]
 > db.scores.count( { score : { $lt : 10 } } )
Should be 0
> db.scores.count( { score : { $lt : 20 } } )
Should be same as we got before by finding scores < 10
> db.scores.count( { score : { $gte : 60 , $lt : 70 } } ) 
Should be sum of previous result, plus the ones we previously found in the range [50, 60)
EXAMPLE [developer]: 
Imagine a simple analytics data model that, for each url, stores the total number of pageviews and the number of pageviews per user agent. How could this be modeled? What query would produce this?
ANSWER: 
Model: { _id : { url : ‘...' } , total_views: 47 , chrome : 20 , firefox : 15 , … } 
db.user-agent.update( { _id : {url : ‘...' } } , { $inc : { browser_name : 1 , total_views : 1 } } , { upsert : true } )
FOLLOW-UP QUESTION:
What if you wanted to add the day to the schema (or hour)?
ANSWER: 
Model: { _id : { url : ‘http://...' , day : 123} , chrome : 20 , firefox : 15 , … } 
db.user-agent.update( { _id : {url : ‘http://...' , ISODate().toISOString().slice( 0 , 10 ) } } , { $inc : browser_name : 1 , total_views : 1 } , { upsert : true } )  # slice to 13 if you want the hour, too

Delete
Objective: Students will be able to remove documents from a collection.

Deleting something is pretty simple. If you want to remove a set of documents, you can remove any that match a .find() query using .remove() instead.

For example, suppose our collection were:

> db.monty.find()
{ "_id" : 1, "noun" : "swallow", "verb" : "fly" }
{ "_id" : 2, "noun" : "coconut", "verb" : "clap" }
{ "_id" : 3, "noun" : "coconut", "verb" : "fly" }
{ "_id" : 4, "noun" : "swallow", "verb" : "clap" }

and you used the query:

> db.monty.remove( { noun: "coconut", verb: "clap" } )

Your collection will now be:

> db.monty.find()
{ "_id" : 1, "noun" : "swallow", "verb" : "fly" }
{ "_id" : 3, "noun" : "coconut", "verb" : "fly" }
{ "_id" : 4, "noun" : "swallow", "verb" : "clap" }

If you want to remove an entire collection including metadata such as indices, you can simply type db.collection.drop(). Also, if you want to delete most of the documents (but not all) from a large collection, it may actually be faster to copy those documents you want to save to another collection, drop the original collection, and then insert them back into the original collection. You will have to rebuild indices, but otherwise you should be good.
Otherwise, db.collection.remove() will delete documents. If you give it no argument, it will go through the entire collection dropping documents, but if you pass it a document, it will only delete those files that match the document.

One of the tricky things to remember, though, is that unlike db.collection.update(), which only updates one document by default (and you can pass {$multi: true} to make it update all documents that match the query), db.collection.remove() will remove all documents that match the query by default. If you want to have it affect only one document, you can pass it {justOne: true} after your document to match.

Bulk Operations (new in 2.6)

Objective: Students will know how to perform bulk operations in the shell, and will understand that they can already pass bulk operations into their drivers.

A new feature in MongoDB 2.6 is bulk operations. You can perform bulk operations by instantiating a bulk object with an assignment such as:

> var blk = db.collection.initializeOrderedBulkOp()

or 

> var blk = db.collection.initializeUnrderedBulkOp()

These bulk objects will behave exactly the same until you execute them. Prior to that, though, you will want to pre-load your operations. You can do this with, for example:

> blk.insert( { a : 1 } )
> blk.insert( { a : 2 } )
> blk.insert( { a : 3 } )
> blk.find( { a : { $exists : true } } ).update( { $set : { b : 1 } } )  # Updates all documents
> blk.find( { b : 1 } ).updateOne( { $set : { c : 1 } } )  # Updates one document
> blk.find( { c : { $exists : false } } ).removeOne()  # removes 1 document
>blk.execute( { w : 1 } )  # for example

With blk.execute(), we will see the difference between an ordered bulk insert and an unordered one. For an ordered bulk insert, each operation is executed serially. If one of the operations generates an error, only those operations that came before it will be executed; the rest will be abandoned. This is because there is a presumption (with ordered Bulk Operations) that each step may depend on one or more of the preceding steps.

If you are working with an Unordered Bulk Op, all operations will occur in parallel (within hardware limits). Any one exception will stop one operation from occurring, but will not affect other operations. 

Individual drivers will often allow you to perform multiple operations at once, and have been able to do so for quite some time. See your drivers' insert, update, and remove methods for more information.

Database Locking
Objective: Students will understand the difference between read and write locks, how exclusive they are, and which take priority.

Something to think about that is more of a systems-y thing is the state of the server with respect to locks. Read locks can happen in parallel, and only prevent writes. Write locks prevent anything else from happening. In other words, you can have lots of reads, but only one write at a time.
This type of locking mechanism can be called:
Readers-writer (notice the plural ‘s' is only on readers) lock
This is our preferred term at MongoDB
Multi-reader lock
shared exclusive lock
Also, MongoDB locks are writer greedy. That is, if the system is waiting to give a lock to both a read and a write, it will prioritize the write.
Finally, locks are on a per-database level. If you've got 3 databases running on a machine, and one of them acquires a write lock, you can still perform reads or writes on the other two. Also, when we talk about sharding later on, the locks are only on a single machine. If you are working with a sharded collection, one shard might impose a write lock, but you can still read on the other shard. 
If the students are interested in the details, they can go to:
http://docs.mongodb.org/manual/faq/concurrency/



Indexing
Objectives: Students will understand the advantages and disadvantages of indexing, when indices are redundant (and should be deleted, if present), and how to choose effective indices. Finally, they should be able to evaluate the utility of an index for a particular query using the db.collection.find().explain() method.

NOTE:
It might be good, at this point, to ask how many people in the room are familiar with indexes in a relational database. If they all are, just explain that indexes work the same way in MongoDB, so you (the instructor) can skip the explanation and jump straight to the syntax.

Now we should discuss one of the most important ways for you to maximize the speed of your queries (and the seek portion of update() or findAndModify()): Indexes. 

In the absence of an index, any time you want one (or more) documents that match a query, MongoDB will have to scan through all of the documents, one by one, checking each. This is murder for database performance. If your data set is too small to fit into memory, you need to page some of your data in and out as you do these scans. This is double murder. Navigating an index is extremely quick. You can find out which documents match your query, and where in memory (or on your drive) the document is, and then you can go there and look at that. 

An index is a B-tree (Not a binary tree!) that we build that allows us to look up, for fields that match the index, where the documents are stored. Building an index doesn't change the order of documents on disk, and you can have multiple indices that internally order documents differently at the same time. This is not a problem because, as I said, building an index doesn't entail moving a document. An index will tell you where on the disk a document is. So, how does an index work? Let's look at the following: 

SHOW
db.tweets.find({"user.followers_count": 1000}, {_id: 0, "user.name": 1})
I limited it to user.name so that the documents aren't hard to visually parse.
8 documents get returned.

Now, if we want to explore what the database does in this case, we can use the .explain() method on the query.

SHOW
db.tweets.find({ "user.followers_count" : 1000 } ).explain()
n: 8
nscanned : 51,428
nscannedObjects: 51,428
scanAndOrder: false
millis : lots (80-140 for me when I made this)
Now, db.tweets.ensureIndex( { "user.followers_count" : 1} )

The first thing you want to look at is n. it's 8, which is the number of documents that match the query. 

The next thing you want to look at is nscannedObjects, which is the number of documents that were searched during the query. You'll notice that it was very big. This is evidence that this query would benefit from an index.

Another thing you can look at is nscanned, which can include index entries or actual documents that you look at. Sometimes you to scan an index for a field, which is usually faster than loading a lot of documents into memory, because (1) index entries tend to be smaller than documents, and (2) for a large collection, it's likelier that your index is in memory than that your entire collection is.

Let's build an index on this collection.

SHOW
db.tweets.ensureIndex( { "user.followers_count" : 1 } )
db.tweets.find({ "user.followers_count" : 1000 } ).explain()
n : 8
nscanned : 8
nscannedObjects : 8
millis : 0-1

You can see that there was a BIG improvement. We didn't look at a single document except the ones we needed (nscannedObjects is 8). We didn't even have to scan through the index to find what we're looking for (nscanned is 8). All we had to do was jump to the correct part of the index, find out what we needed, and then load those documents into memory.

DBA's are used to thinking about this, but in MongoDB, developers need to be a lot more involved in the creation and use of indices.

There is a tradeoff between reads & writes that one makes when one uses an index. Indexes favor reads heavily, but they do make writes a little longer for each index. Inserts have fields that need to be added to the index, updates have to potentially move an entry within the index. On the other hand, some writes might be faster. For an update() to a single document, for example, you don't need to scan an entire collection to find a document before finding it and updating it. 
SHOW
a GREAT blog post about this:
emptysqua.re/blog/optimizing-mongodb-compound-indexes/
Talk them through it. It's a great description of how our indexes work.
Better yet, do it in your terminal step-by-step, and have them follow along.


Here's how a B-tree works. You put in a value. It's got a sensible sort order (in this case, ASCIIbetical for strings, numbers are pretty straightforward, etc). So you walk the B-tree looking for its place. Supposing that you were looking for a value of 28. You go to the top bucket of the B-tree. It's greater than 25, so you look in the third sub-bucket. It's between 26 and 35, so you look for it in the bucket between them, and you find it, and you find that it's mapped to a memory location. You've found your document.

If you're looking at a big collection, and only a few documents match the query, they can be a huge help.

I've drawn this diagram so that most of the buckets contain 3 sub-buckets, but there's nothing special about the number 3 here. Buckets can contain as many sub-buckets as they please. All of this is handled behind the scenes, though. 

Let's ask another question: what if knowing the value of just one field isn't enough? What if we need to know two or more fields? Then we implement what's called a compound index.

With a compound index, you take the index on two fields, but it's not the same as just having two indexes, one on each field. Instead, it's ordered. It's one field, then the other. If you want a third field to be in the index, then it's one, then the second, then the third. And for each of these, you have to pick an order: low-to-high, or high-to-low. This matters a lot less for a simple index, but for a compound index, it can make a big difference, especially when you want to sort. Let's look at an index creation statement: 

> db.collection.ensureIndex( { a : 1 , b : -1 , c : 1 } )

This creates a triply compound index, with a sorted canonically, b sorted anticanonically, and c sorted canonically We'll talk a little about what we mean by that, later, but just like you can sort canonically or anticanonically, you can index the same way, and your index needs to be compatible with your sort. 

Now, suppose, you want to perform the following query:

> db.collection.find( { a : 22 , b : 33 , c : "hello"} ) 

The index will get you exactly what you want: those document that match. 

So will this query: 

> db.collection.find( { a : 22 } ) 

But this query won't work. At all: 

> db.collection.find( { b : 22 } ) 

Now, this is a little surprising to people who have never seen a compound B-tree. Why does the index work for a but not for b? And to find the answer, you need to look at the structure of the b-tree. Let's take an analogy: the phone book.

Now, the phone book is ordered by two fields, the first and last names. But it's not just in any old order. It's last name, then first name. And it's ordered, so both of them are in alphabetical order. Neither first name nor last name are backwards (though we could have done one of them in reverse alphabetical order!). In MongoDB, we would have created a phone book-style index with:

> db.collection.ensureIndex( { last_name : 1 , first_name : 1 } )

OK, so look at how we might use this.

Suppose you want to look for Cercei Lannister. How many names would you need to check? Would you need to scan the whole book? No! You only need to look at the Cercei Lannisters. There might be only one. You skip almost all of the book.

But what if you want all people named Lannister? Is that much harder? No! It would require more memory to hold them, but it's still not much harder! You start at the beginning of Lannister, you end with Lannister, you ignore everyone else. You are still only checking one small part of the phone book.

Now, what if you needed to find all people with the first name of Cercei. Any last name is fine, but their first name MUST be Cercei. This is really only a small fraction of the people around. How many names do you need to check?

Basically, all of them.

The phone book is of NO help, because it is organized as an index with compound keys last_name, first_name.

Also, if you want to sort on last_name, then first_name, you're great! You just use the order in the phone book! Alternatively, if you want to sort backwards on both, you're still great! You start at the end of the phone book, and go backwards. But if you want to sort forwards on last name, then backwards on first name, that's trickier. You can't just use the order in the book, you need to keep track of everything. You have to do an actual in-memory sort. Same thing if you want to sort primarily on first name, then on last name. The index just won't help. You have to do everything in-memory.

So a compound index isn't a panacea. If you sometimes sort by first_name then last_name, but sometimes by last_name then first_name, you might need two indexes. On the other hand, if you sometimes sort by last_name then first_name, and you sometimes sort by just last_name, that one compound index will work for both. 

And this is good, because (and this is a very important thing to remember) indexes aren't free. They take up memory. Every byte you spend on an index is a byte of documents you don't get to have in memory, and that means it's more likely that when you want to retrieve a document, you have to hit the hard drive. Or worse yet, you might have so many indexes that not all of them can fit into memory, and then adding another one means that you spend more time reading other indexes off of the hard drive every time you need them. So often indexes are worth it, but you can definitely get into a situation where you have a lot of indexes, and you shouldn't build a new one.

And compound indexes do take up more memory than a standard index. They're great if you use that memory, but not so great if you're really not using them. So only build indexes you need, don't just go building indexes on every possible combination of things.

WRITE: 
Limitations of a compound index:
You can't use hashed index keys
They take up more memory than basic indices

Another thing to keep in mind is that you can have, at most, 64 indexes
You should NEVER be anywhere close to that upper bound. 
Writes will start to take FOR EVER at somewhere between 20-30.

Why? Indexes have another cost. They don't just take up memory (though they do that, too). They have to get modified any time a document gets created, or updated in such a way that its indexed field changes, or if it moves. And potentially, this can happen for EVERY index.

So use your indices sparingly! 

For example, if you have both of the following indices:
key: { a : 1 } 
key : { a : 1 , b : 1 } 

you can kill the first. The second will already allow you to index on a alone. You should NEVER have a pair of indices that look like this.

On the other hand, these two indices are NOT redundant: 
key: { a : 1, b : 1 }
key: { b : 1 }

The first index will not work for queries on only b. So maybe (depending on your use case) you might want to build this pair of indices.

So, when is an index worth the trade-offs? Let's consider the following:



Ideally, your entire data set will be small enough to fit in memory AND your index will fit in memory. Unless you only have a little data, or you deal with a MASSIVE infrastructure budget, that's basically never going to happen. The fact that you're considering MongoDB means it's almost certainly not the case. A secondary possibility, and almost as good, is to ensure that your indexes, and a working set, fit into memory. From time to time you'll have to hit the hard drive, but your performance will still be very good for the vast majority of your queries.

WRITE:
Indexing concepts
Primary index
_id
Basic index
Any index that's on just one field
Compound index
Any combination of fields
Hashed index
Can't be a compound index
Great for sharding, especially if you have a monotonic key (2.4+)
Text indices
Great for searching (2.4+)
2-D Geospatial Indices
Many people don't use them, but those who do love ‘em
TTL Indices
"Time to Live"
e.g., 2 days
Deletes things from a collection (not just from an index) that are too old
Guarantees that every document will be around BEFORE the expiration datetime
Things may linger for a bit; by default, the deleting thread runs every minute or so.
Covered query
All of the data you need is in the index; no need to use any other data.

But how do we know if we're actually using our indices or not, for a particular query? We use the explain() method.

db.collection.find().explain()
Basic cursor = full table scan
n = how many docs found?
nscanned = how many docs looked @
scanAndOrder - should be false; you don't want to order them in memory.
indexOnly: covered query?
Look @ the emptysqua.re blog
.sort().explain()
Blog
Blog is better than what the book has, currently.


What if you want a query to use a particular index for its query?

find().hint()
db.collection.find().hint({key_found_in_index:1})
Tells the collection to use a particular index when multiple indices are plausible. This will prevent it from occasionally running parallel jobs in order to race them against one another.

(Maybe be ready to talk about the following, if they come up)
Unique Indexes
db.collection.ensureIndex({x:1}, {unique: true});
insert: {x:5}, {x:10}, {y: 7}, {x: 10} (won't work), {y: 19} (won't work)
Sparse Indexes
Good for when many docs have no key or value

Multikey Indexes
A multikey index is an index on a field where the value is an array. In this case, you needn't match the exact array with your query by default; instead, a query will return the document if even one element matches your array. 

For example, suppose that we have the following collection: 

> db.multikey.find()
{ "_id" : 1, "array" : [ "spam", "eggs", "fizz" ], "string" : "Eric Idle" }
{ "_id" : 2, "array" : [ "fizz", "spam" ], "string" : "Terry Jones" }
{ "_id" : 3, "array" : [ "buzz", "fizz" ], "string" : "John Cleese" }
{ "_id" : 4, "array" : [ "spam", "fizz", "eggs", "buzz" ], "string" : "Terry Gilliam" }
...

The "multikey" field has up to four values in its array: "spam", "eggs", "fizz", and "buzz". Each has an independent 50% chance of being in any document, but the odds of only one being in a document are 1 in 24, or 1/16. There are 1,024 documents in the collection.

Next, let's build an index. 

> db.multikey.ensureIndex( { "array": 1 } )

And we'll do a find for the array field equal to [ "spam"]:

> db.multikey.find({ array: ["spam"] } ).explain()
{
	"cursor" : "BtreeCursor array_1",
	"isMultiKey" : true,
	"n" : 45,
	"nscannedObjects" : 526,
	"nscanned" : 526,
	"nscannedObjectsAllPlans" : 526,
	"nscannedAllPlans" : 526,
	"scanAndOrder" : false,
	"indexOnly" : false,
	"nYields" : 4,
	"nChunkSkips" : 0,
	"millis" : 1,
	"indexBounds" : {
		"array" : [
			[
				"spam",
				"spam"
			],
			[
				[
					"spam"
				],
				[
					"spam"
				]
			]
		]
	},
	"server" : "will-macbook-air.local:27017",
	"filterSet" : false
}

We can see that 45 documents were returned, not too far from the 64 we'd expect on average. 

On the other hand, let's do the very similar query, 
> db.multikey.find( { array : "spam" } ).explain()
{
	"cursor" : "BtreeCursor array_1",
	"isMultiKey" : true,
	"n" : 526,
	"nscannedObjects" : 526,
	"nscanned" : 526,
	"nscannedObjectsAllPlans" : 526,
	"nscannedAllPlans" : 526,
	"scanAndOrder" : false,
	"indexOnly" : false,
	"nYields" : 4,
	"nChunkSkips" : 0,
	"millis" : 1,
	"indexBounds" : {
		"array" : [
			[
				"spam",
				"spam"
			]
		]
	},
	"server" : "will-macbook-air.local:27017",
	"filterSet" : false
}

Here, we can see that 526 were returned, or about half of the 1024. 

The multikey index works like this because when the value of the query isn't an array, but the value of a document is, the query will return the document if the value in the query is the same as any of the values in the array in the document. 

A multikey index will index all of the values in the array in the field. This can, potentially, make for a very large index. 

If you want a compound index that is multikey on one of its fields, that's fine.

If you want a compound index that is multikey on two or more of its fields, you're almost certain to get an error*, because the number of index entries scales as the product of the lengths of the two arrays, which can quickly become prohibitively large. The database will stop you from making this potentially fatal mistake.

*If someone asks, you won't get an error if no single document has both fields with arrays for values.


Text Indices
Objective: Students will be able to create text indexes, see an example of text index usage, and understand the analogy between text indices and multikey indices.

A text index is an index on the words you find in text. It works a lot like a multikey index, with the words in a text field being like the elements in the array: any one of them can match a query, though unlike a multikey index, you need to specifically invoke the text index.

You create a text index a little bit differently than you create a standard index: 

> db.collection.ensureIndex( { a : "text" } )

At this point, you can treat the "a" field as a multikey index with all of the words in the index as values. You can, at some later point, query the field with the $text operator. For instance, the query

> db.collection.find( { $text : { $search : "swallow" } } )

will find any documents with the word "swallow" in the "a" field.

So, for example, if we had the following documents:

> db.collection.find()
{ _id : 1 , a : "What… is the air-speed velocity of an unladen swallow?" }
{ _id : 2 , a : "What do you mean? An African or a European swallow?" }
{ _id : 3 , a : "Huh? I… I don't know that." } 
…
{ _id : 45 , a : "You're using coconuts!" } 
{ _id : 55 , a : "What? A swallow carrying a coconut?" }

we then the query would return:

> db.collection.find( { $text : { $search : "swallow" } } )
{ _id : 1 , a : "What… is the air-speed velocity of an unladen swallow?" }
{ _id : 2 , a : "What do you mean? An African or a European swallow?" }
{ _id : 55 , a : "What? A swallow carrying a coconut?" }

Similarly, we would have

> db.collection.find( { $text : { $search : "swallow coconut" } } )
{ _id : 1 , a : "What… is the air-speed velocity of an unladen swallow?" }
{ _id : 2 , a : "What do you mean? An African or a European swallow?" }
{ _id : 45 , a : "You're using coconuts!" } 
{ _id : 55 , a : "What? A swallow carrying a coconut?" }

will find any documents with the word sparrow or the word coconut. You can look at the documentation to find out how to search for phrases, or exclude words.

Finally, the search algorithm has a score that it assigns, and the documents can be ordered by that score so that the ones with the most matching words will be highest. It uses a vector ranking algorithm. 

Example:

> db.collection.find({ $text : {$search: "swallow coconut"}}, {textScore: {$meta: "textScore"}}).sort({textScore: {$meta: "textScore"}})


Query Plans
Objective: Students will understand when and how a query plan is created, when they are re-created, and what effect they will have on queries going forward. The student will also know how to override a query plan with hint.

Query plans are MongoDB's way of automatically ensuring you're getting the most out of your indexes. Suppose, for example, that you're doing a query that searches for 3 fields: a, b, and c. 

Let's suppose that your indexes were set up in the following way: 

> db.collection.ensureIndex( { a : 1, b : 1 } ) 
> db.collection.ensureIndex( { c : 1 } )

So you've got a compound index on a and b, and then a simple index on c.

Let's also suppose that you've never done a query on these 3 fields before, and we'll take a look at what happens when a query does occur.

Suppose that you run:

> db.collection.find( { a : 13 , b : 22 , c : 19 } )

What are some reasonable ways to figure out whether to use the a_1_b_1 index, the c_1 index, or neither?

It will run the query first using the a_1_b_1 index, and then scan the documents it finds for a match on c.
It will run the query first on c, and then scan the documents it finds for a match on a and b.
It will do a full table scan, and check each document for a match on a, b, and c.

Now, without knowing more information, it's impossible to say which of these plans will win the race in a particular situation, though the full table scan shouldn't win in most reasonable situations. So MongoDB will try all 3, and see which one finishes first. 

It will store these results in what's called a query plan, and from that point onward, similar queries will be run with the winning technique.

A new query plan will get built using this testing method once 1000 writes have occurred, you reIndex, you build or drop an index, or the mongod process restarts. 

If you want mongoDB to use a particular method, you can give it a hint. For instance, 

> db.collection.find( { a : 13 , b : 17, c : 13 } ).hint( { c : 1 } ) 

will force it to use the { c : 1 } index. 

So we call it a hint, but it's really insisting (rather than hinting) that the DB use a particular index for a particular query. Hints will always override query plans. 

Index Filters (new in 2.6)

Objective: Students will understand how Index Filters work and when they apply. They will also understand their priority vis-a-vis Query Plans and hints.

New, in MongoDB 2.6, an index filter is a little bit like a hint. You give the database a query shape, and an index filter, which specifies those indices that the query plan can legitimately try; those outside the plan don't get tried.

If an index filter exists, it has a higher priority than a hint(). Index filters exist until the server process dies, and do not persist. 

Since filters are accessed through db.runCommand, you won't remember how to use them. Look them up in the documentation if you need to put them in place.

Because they override hint(), be sure to use query plans sparingly. 

Index Intersection (Include at a point TBD)

Objective: Students will be able to understand how index intersection works, and will be able to predict when MongoDB is likely to make use of intersection.

Index Intersection is when a database uses two indexes to fulfill a query. For example, suppose we have, in each document, two fields, "a" and "b", each of which can take on an integer value. 

We'll begin by indexing each of those fields: 

> db.collection.ensureIndex( { a : 1 } )
> db.collection.ensureIndex( { b : 1 } )

So now we've got an index on each, but no indexes on both. Let's suppose you're doing a query such as:

> db.collection.find( { a : 3 , b : -5 } )

If we had a compound index on a and b, that would be ideal, but in this case, we don't have one. If this were the first time such a query occurred, MongoDB would build a  

Geospatial Indices (Optional Lesson)
Objective: If students are interested, they will learn the basics of how geospatial indices work in MongoDB.

Ask if anyone is interested in Geospatial Indexes. If not, move on, but if so, here are the key concepts:

First, there are "Flat" (x-y plane) "2d Index". They use (latitude, longitude) and are very good close to the equator, but may cause problems close to the poles, so don't use them to map out Antarctica.

Next is the "2d Sphere" (spherical surfaces)
Can have points, lines, polygons to generate areas.
Will determine distances


Day 2

Schema design
Objective: Students will be able to evaluate the utility of a particular schema from their expected usage model, and understand the importance of a good schema. 

This should take about ½ a day.

Now we're going to look at schema design. The main question that you want to ask, with schema design, is this: are we going to optimize this for reads, or for writes?

In many cases, you want to think about your problem, and even begin building your application, before building a schema. 


Let's look at creating an ecommerce site. 
We are selling things. So, we're going to need to figure out what data we're going to need.

EXERCISE: ecommerce Site
In this group exercise, we're going to take what we've learned about MongoDB and try to come up with a basic but reasonable data model for an e-commerce site. For users of RDBMSs, the most challenging part of the exercise will be figuring out how to construct a data model when joins aren't allowed. We're going to attempt to model for the following entities and features:
Products. The core of an e-commerce site, products vary quite a bit. In addition to the standard production attributes, we'll want to allow for variations of product type, along with custom attributes.
Product pricing. Current prices as well a price histories.
Product categories. Every e-commerce site includes a category hierarchy. We need to allow for that hierarchy, and we also must persist the many-to-many relationship between products and categories.
Product reviews. Every products has zero or more reviews, and each review can receive votes and comments.



Have the students build their requirements (They should have something similar to the following)
Products
Price (+ historical prices)
Name
Attributes
Comments
(Ranking?)
Categories
Users (We won't be doing the schema for users)
(Instructor will probably need to break the students up into groups of 3-4, or else they won't do it themselves.)
Give them ~1 hour to develop a schema. Check up on them every 10 minutes or so; they might be using a relational schema, or something similar.
Have them present (~5 minutes per group to present, +5 minutes' discussion)
Things to consider:
People will want to search by categories
People will want to view similar things
People will want to see comments with the thing
Inventory # is a good idea
Things are bought much more often than created, and read much more often than bought.
Indexes: where do they go?
Good idea:
Reviews: only store the top 1-5 most useful, show those to customers, then have a link to "all reviews" or "click for more" or something that retrieves them ALL from the "Reviews" collection.
EXERCISE: Card Catalog System

Let's create a design for a Library card-catalog system. What data would we need?
Write their answers
If they don't include all of the following, suggest it:
Author
ISBN
Title
Copyright date
Publisher
Let's add information about authors, too.
Authors
Name
Birthdate
City of residence
Biography

OK, that's the information we'll need, go out and build a schema!

(Probably their schema will end up looking something like this)


Other Exercises:

use Nathan's Schema Design Workshop

Things to Consider when Building a Schema

1st: How does your app use your data? (diagram)

Each cell is a doc; the green stuff shows the data in the doc that the app actually uses. 
You want to have data saturation in your document

In other words, if you're only using 10% of your data in each document, you're probably doing it wrong. Every time you load a document into memory, it's taking longer than it should, it's taking up more memory than it should. Try to build your document structure around only of the data you're going to use at one time, but make sure you limit your number of queries, too. Doing the same hundred queries each time you need information is just as bad as pulling a lot of stuff you don't need but only doing one query. Try to strike the perfect balance. 



Dealing w/ dynamic attributes

For example, suppose you've got a collection that contains things you sell: CD's, pictures, but also mp3's. So a given collection might need to describe:

Size : ‘10 x 9'
Weight : ‘5 lb'
Color : ‘red'
…
what if attribute isn't relevant?
what if there are many attributes?

do we index this? We cheat, with multikey indices!
attrs: [{k: ‘size' , v : ‘10x9'}, {k : ‘weight' , v : ‘5 lb'}, …]
Now can index easy and have unlimited dynamic attributes! db.collection.find({"attrs.k": "size"})
3 or more separate indexes can all be combined easily!


There are some potential problems any time you're dealing with arrays, of course. Keep in mind, your index will have all of these attr.k or attr.v values. Indices can get pretty big in these cases.


Replication - Building Redundancy into your System
Objective: Students will understand the purpose of replication, and the roles of the various replica set members that they can set up.


Here we have an application talking to the primary of a replica set. It writes data to the primary, and that data gets replicated to the secondaries. If the primary goes down, a secondary will quickly step up, become a primary, and you're great!

Of course, as I've drawn this, your primary and your secondary are all in the same place. What if there's an earthquake, or a power outage, or an EMP goes off? Then… well, then you've got a problem.

Data Sets

So, let's try to build  a little more redundancy into our system.



Now, what happens if the primary goes down? 
Answer: we're OK

What if we lose DC2?
Answer we're OK

What if we lose Data Center 1?
Answer: we're not OK
So, how can we avoid arbitrary data center loss?

We need 3 data centers, with 1 member in each data center. There is no way to be completely resilient against the loss of any single data center without splitting your servers up like this. 



One common RS mistake to avoid is making the secondary be less powerful than the primary, "because it has a lower write load."

In fact, writes to primary ALSO go to secondaries
In case of failover, a secondary may become a primary; that's the point.

So if anyone makes a secondary less powerful than the secondaries really doesn't have any real redundancy.


OpLogs

Every Replica Set has an OpLog. This is typically a fixed size. Suppose our OpLog is 1 GB.
When I give a command (db.insert(some_document)), the OpLog stores it, along with a timestamp & sequence number.

Let's start drawing oplog records in a simplified format: 


Ordinarily, a secondary would try to stay as up-to-date as possible, stepping through the oplog one at a time shortly after each operation gets written by the primary.

But suppose a Secondary was present initially, but it has been unavailable while the OpLog got written. looks at this, and it says "OK, what's your latest command? ‘Cause I'm ready for #1." The primary will be like "100", and the Secondary would be like, "OK, give me all 100.

So then we get something like this:







PRIMARY				Secondary #1		Secondary #2   -->   -->


Now, if the Secondary #2 has its lowest latency to the other secondary, it'll get the oplog from secondary #1 instead of from the primary. This might happen if, say, the primary were in Europe, secondary #1 in New York, and secondary #2 in LA

Now, let's suppose we only have room for 100 documents in our OpLog. Now, the primary will overwrite Operation 1 with Operation 101.


Now, let's say a secondary goes out.

Now, let's say another 200 commands come in. 
The Primary and the second Secondary are at command # 301, and then the downed Secondary comes up.

PRIMARY				Secondary #1		Secondary #2   -->   -->




At this point, this secondary says, "OK, can you give me command 102?" and the Primary and the other Secondary are at 300, and have events 201-300. 
Now, the only way to get the secondary back in sync is with a FULL re-sync: all the data, plus the OpLog.


PRIMARY				Secondary #1		Secondary #2   -->   → 		





The Secondary does a full re-sync from all of the Primary's data, and copies the OpLog, and then begins stepping through the OpLog, one by one.


Now, clearly there's an issue here. What if writes occur partway through the primary's scan, but then are listed at the end of the OpLog?

Answer: the writes themselves are NOT stored in the OpLog. Insted, "Idempotent" versions of the operations

Idempotent means that repeats of the original statement don't do anything. It's about setting a field to a particular value, rather than (say) incrementing or decrementing it.

Some people have issues with Replica Sets that are under such heavy load that by the time a sync occurs, they fall off the oplog. Usually this is evidence that you need a longer OpLog.

By default, the OpLog is 5% of disk space. 

One thing that you can do in order to ensure that your data is replicating, is to set the write concern that are greater than 1. That way, if you run into a problem with the primary

Then you can go on, business as usual. You've already written things. 

If you don't do this, you can get a situation where the primary goes down, and some writes occur that are not communicated to any secondaries.

So suppose that my Primary goes up to 400, but the secondary is only up to 399 when the Primary goes down. The Secondary becomes a Primary at that point, and then goes forward. Its next write is OpLog operation #400. 

Now we have two #400's. The state of the database is in conflict. What happens? Well, when the old Primary comes back online, the conflict is noted, a process we call "Rollback". 

If the old primary falls off the OpLog, data about that conflict is lost, as the old primary must take a snapshot and then follow the OpLog of the secondary.

Elections

Bias them by giving different priorities to different members
If one has the highest priority, it will become primary as soon as it catches up after failover.
Bias them by giving some members 0 votes
A primary is elected with a majority of votes, so if this particular 0-vote node goes down, it won't affect the behavior of elections. 

Other ways to customize Replica Sets
Hidden
Tags
Allows you to set read preference in your application
SlaveDelay

A good note here: reading off of secondaries DOES NOT buy you anything! Writes are replicated in secondaries. Reads can be done in parallel, and reads don't require a lock. 

EXERCISE
We're now going to create a Replica Set.
Reference: http://docs.mongodb.org/reference/replica-configuration/
Reference: http://docs.mongodb.org/reference/method 
mkdir /data/rs1
mkdir /data/rs2
mkdir /data/rs3
mongod --replSet myReplSet --logpath "1.log" --dbpath /data/rs1 --port 27017 --oplogSize 200
mongod --replSet myReplSet --logpath "2.log" --dbpath /data/rs2 --port 27018 --oplogSize 200
mongod --replSet myReplSet --logpath "3.log" --dbpath /data/rs3 --port 27019 --oplogSize 200


At this point, we're up to 3 mongod's, all with the same replSet, but they don't know this yet. In production, we'd bring up these three servers in three boxes. They're not yet aware of each other, but that's fine.

SHOW
mongo --port 27017
var config = { _id : "mySet",  members: [ {_id : 0 , host: "localhost:27017" } , { _id : 1 , host : "localhost:27018" } , { _id : 2 , host : "localhost:27019" } ] }
rs.initiate( config )
rs.status()
Do this several times, until you have a primary and 2 secondaries.
exit
mongo --port 27018
db.test.insert({a: 1})
Not primary!!
mongo --port 27017
db.test.insert({a: 1})
db.test.count()
1
exit
mongo --port 27018
db.test.find()
error!
rs.slaveOk()
db.test.find()
There it is!!
db.getReplicationInfo()
Show them the oplog
use local
db.oplog.rs.find()
there it is!
exit
mongo --port 27019
config = rs.conf()
config[1]["priority"] = 2
Have I changed my config? Not yet!
rs.reconfig(config)
Notice that the primary is now secondary!
And port 27018 is now primary!
Now, to kill the primary
ps ax | grep mongod
Find 27018 and kill it!
Now, look for the primary (27017 or 27019). There it is! it's taken over!!

Up until this point, we've only talked about primaries and secondaries in our replica sets. However, there are a number of other types (or modifications to these member types) that we can make use of.

A full list can be found here:
http://docs.mongodb.org/manual/reference/replica-states/

But we've written a bit about the most common situations, below.

Arbiters
One of the things you'll notice is that a replica set requires a strict majority of its members to elect a primary. So, if you have a 2-member replica set, and one goes down, the other cannot elect itself primary. For a 4-member replica set, you would require at least 3 members, adn for a six-member replica set, you would require four members. Any even-numbered replica set population is therefore less stable than the odd-numbered replica set below it, because it can tolerate the same number of missing members, but it has more members that can potentially fail.

Replica Set Population	Max Tolerance for Disabled		M.T. with 1 Arbiter
1				0					0
2				0					1
3				1					1
4				1					2
5				2					2
6				2					3
… and so on.

But sometimes we'd like to be able to have a 2 or 4-member backup. What do we do? We add an arbiter. You will NEVER need more than one, and you should only add one if you have an even number primary plus secondary members.

The arbiter won't store data, so it can be a very lightweight (and cheap!) machine. If you want to be tolerant of a data center failure, you should put your arbiter in a separate data center than either your primary or secondary, as you would with a standard three-member replica set.

Modifications of Primary and Secondary Members
slaveDelay: 
Describes the number of seconds "behind" the primary that this replica set member should "lag." Use this option to create delayed members, that maintain a copy of the data that reflects the state of the data set at some amount of time in the past, specified in seconds. Typically such delayed members help protect against human error, and provide some measure of insurance against the unforeseen consequences of changes and updates.

Read Preference (WRITE THIS)

Aggregation

Let's take a few minutes and look at the aggregation pipeline. The aggregation pipeline is used to pull data from the server that is not explicitly stored, but can be calculated from explicitly stored data. It is present so that you don't have to pull a lot of data over the network and then do your calculations in-app. Instead, you can use the server's power and just get the answer. For those of you who are coming from the SQL world, Aggregation is MongoDB's answer to the GROUP BY statement.

When pulling data from a collection, you've got a few options:

Built-in commands are:
.find()
.find().count()
.distinct()
MapReduce
Hadoop
.aggregate()

Option: First, start with a demo of MapReduce, which has a trendy name but it's not as cool as Aggregation. Then show them the BEST way to do things (Aggregation).

SHOW
use digg
db.stories.aggregate( [ { $match : {  } } ] )

Returns things that match this

On MongoDB 2.2 or 2.4, the result set MUST be < 16 MB, our size limit for documents, but intermediate steps can make it larger. 

For MongoDB 2.6, you no longer face this limitation, but the total set must be < 100 MB. If you want to get around this, you can, but you need to go to the disk. 

The aggregation framework is pretty simple: 

SHOW
db.collection.aggregate( [ { stage_ 1 } , { stage_2 } , … ] , { options } )

Its output is typically a cursor pointing to your result set of documents, but you can also write that result set to a new collection, or replace an existing collection with this result set (you cannot append to a collection as of MongoDB 2.6.0).

Aggregation stages are represented by their top-level operator. We have several:
$project
$match
$limit
$skip
$unwind
$group
$sort
$geoNear
$out
$redact

A lot of aggregation stages will do the same thing as some of the read operations you're used to. For instance:

SHOW
db.stories.find( { "topic.name" : "People" )

will get you the same result set as

SHOW
db.stories.aggregate( [ { $match : { "topic.name" : "People" } } ] )

And

SHOW
db.stories.find( { } , { _id : 0 , e : 1 } ) 

is the same as 

db.stories.aggregate( [ { $project : { _id : 0 , e : 1 } } ] )

And you can string the stages together, much like you can with cursor methods. For instance, 

SHOW
db.stories.find( { a : 12 } , { _id : 0 , c: 1, e : 1 } ) .sort( { c : -1 } ).skip(12).limit(3)

can be expressed as

SHOW
db.stories.aggregate( [ { $match : { a : 12 } } , { $project : { _id : 0 , c : 1 e : 1 } } , { $sort : { c : -1 } } , { $skip : 12 } , { $limit : 3 } ] ) 

So, why use aggregation? Because there's a lot of calculation you can do on the server that you can't do in a query. The most useful of these is $group.

$group, as you can probably predict, works by grouping together documents. You do this by selecting a new _id, and then all of the documents that match that _id will get grouped together. 

For example, let's go to the zips dataset and do a couple of simple $group operations.

input into your computer: 

> db.zips.aggregate( [ { $group: { _id : { state : "$state" } , num_zips : { $sum : 1 } } } ] )

OK, let's parse this. $state means that we're working with the values found in the state column. So we're grouping together ALL of the zip codes within a particular state. We didn't have to make _id a subdocument, by the way. Things will work just as well with:

> db.zips.aggregate( [ { $group: { _id : "$state" , num_zips : { $sum : 1 } } } ] )
0
(show them this)

but as you can see, the output is a little harder to parse since there's on information conveyed by the _id key. So we'll stick with the first version.

Next thing I want you to notice is that we've got that { $sum : 1 } field. Here, we're saying that for every document you find in the group, add one to this field (and we always start with 0). So, as you can see, we're counting documents for each state with this aggregation, and since there's one document per zip code, we're counting zip codes!

By the way, I told you that putting "$state" into a subdocument with a descriptive field name was a good idea. It also helps if you want to group by two fields. So let's take our original query, and modify it so that we're grouping by both city and state: 

>0 db.zips.aggregate( [ { $group: { _id : { city : "$city" , state : "$state" } , num_zips : { $sum : 1 } } } ] )

(do it for them)

Most of these cities have only one zip code, but if we iterate a few times, we can see that it really is counting. (do it for them)

Q: Now, a pitfall that one might run into: what if we only grouped by _id : { city : "$city" } instead of { city : "$city" , state : "$state" } ? 

A. For a lot of cities, it wouldn't be a problem, but there are cities with the same names in different states, and when this happens, we need to differentiate the state. Otherwise, Springfield, MA and Springfield, OR's zip codes would end up getting grouped together.

So that's great! 

OK, what else can we do? Let's find the population of each city, instead of just knowing how many zip codes each city has!

> db.zips.aggregate( [ { $group: { _id : { city : "$city" , state : "$state" } , city_pop : { $sum : "$pop" } } } ] )

Now, we have a sense of the power and flexibility of the aggregation pipeline. We can group things. We can manipulate them. And we can also filter, sort, skip, and limit them at any stage of the pipeline. 

One limitation of the aggregation pipeline that you should be aware of is that, except for the values that form the _id, you can't just take the existing value and put it into a stage after $group. You need to perform some reducing-style operation such as $sum, $avg. We call these operators "accumulators," and here is the list of them:

Aggregation Accumulators
$addToSet
$first
$last
$max
$min
$avg
$push
$sum

$first and $last don't really act on a group, and it just refers to the first and last value found, so if this will depend on the order in which your documents are examined, you might want to do a $sort before the $group stage.

The next thing I want to show you is the $unwind stage. During this stage, you can take a document containing an array, and turn it into one document for each value in the array. 

Consider the following collection, which we'll name xy, with only document: 

> db.xy.find()
{ _id : "the_only_id" ,  x : 1 , y : [ 1, 2, 3, 4, 5 ] }
> 

If we give the following command, we get: 

> db.xy.aggregate( [ { $unwind : { y : 1 } } ] )
{ _id : "the_only_id" , x : 1 , y : 1 } 
{ _id : "the_only_id" , x : 1 , y : 2 } 
{ _id : "the_only_id" , x : 1 , y : 3 } 
{ _id : "the_only_id" , x : 1 , y : 4 } 
{ _id : "the_only_id" , x : 1 , y : 5 } 

We started with one document, and now we've got 5: one for each element in the y array. The $unwind stage can be undone with $push. So let's unwind and then wind it back up: 

> db.xy.aggregate([{$unwind : "$y" } , { $group: {_id : {_id : "$_id", x : "$x" } , y : {$push : "$y"}} }, {$project : { _id : "$_id._id", x : "$_id.x", y: "$y"}}] )
{ "_id" : "the_only_id", "x" : 1, "y" : [ 1, 2, 3, 4, 5 ] }
> 

And that's how we $unwind!

One thing to keep in mind, which is obvious but still has some implications worth considering, is that after an $unwind, you will have documents with the same _id. The documents returned by an aggregation query don't really form a collection, so this usually isn't an issue, but if you do redirect your aggregation output into a collection (which I'm about to show you), and you didn't $group afterwards, you're going to have a bad time. MongoDB will throw an error.

A new, and very useful aggregation stage, is $out. With it, you take the output of an aggregation pipeline, and put it into a collection. It's got to be the last stage.

> db.collection.aggregate( [ { stage_1 }, { stage_2 } , … ,  { $out : "collection_name" } ] )
> 

$redact (optional lesson) (WRITE THIS)


Day 3
Drivers (optional)

A driver serializes data into BSON and back. It allows you to interact with MongoDB, and should always be used when interacting with the database in a production environment. 

Using a Driver carries two main advantages: 
Connection pooling for all multi-threaded languages
Serialization

The MongoDB shell: is that a driver?
Yes*
Not a rich driver
Single-threaded
If you want a javascript driver, use the node.js driver.
Don't code against the shell. It can be done, but it's not pretty.

Where can we find information on drivers? 
http://docs.mongodb.org/ecosystem/drivers/
Pick one
Java, for example.
Click through to a java API for mongoDB.
See that the page looks like java docs
You can handle, @ application level:
Serialization
Write concern
read and write preferences
schema enforcement
etc.
All connections use TCP sockets
Even ‘unacknowledged'
Examples (for now):
http://docs.mongodb.org/ecosystem/tutorial/getting-started-with-java-driver/
Auth (handled easily)
Write Concern
Each of our API doc pages are written so that it looks like the language doc pages

All of our drivers are designed to be as natural as possible to people who write in that language. Java programmers will feel like they're using java, not like they're using our javascript interface.

Cursors will typically grab a LOT of documents as soon as we start iterating over it, at which point it grabs many docs (100, or <1 MB). Subsequently, it pulls up to 4 MB.

It's literally just an iterator

But you CAN play with it (.sort(), for example) until you actually go out and grab the first document.

Finally, a cursor lasts 10 minutes after your last usage of it (or its creation).

Authentication/Authorization/Access control

Now we're going to talk a little bit about security. A lot of it is outside of Mongodb, like creating secure firewalls, etc.

But within mongodb, we mean running mongodb with --auth, and we mean having a specific account with specific privileges for a specific user. You want to control access: make sure that the individual that is logging in is who you think it is, and that they have the power to do what they need to do, and nothing more.

So here's how our system works: You have an admin database. All power flows from this.  You run mongod with --auth. Then, when you log in for the first time, you need to create a user who has the role of dbAdminAnyDatabase. 

By the way, I should mention at this point that --auth works for standalone systems, but for a sharded cluster or replica set, you need to use keyFile. keyFile implies auth, but also allows members of a replica set or shards of a cluster to communicate and authenticate each other automatically.

For simplicity, let's all just start a mongod with --auth.

$ mongod --logpath /data/db/mongod.log --dbpath /data/db --fork --auth --host localhost --port 27017
$ mongo --port 27017

First, we're going to create an admin account. We'll be making a couple of accounts, so pick names you'll remember for a minute.

> use admin
switched to db admin
> db.createUser( { user : "username" , pwd : "password" , roles : [ "userAdminAnyDatabase" ] } )
Successfully added user: { "user" : "username", "roles" : [ "userAdminAnyDatabase" ] }

Then logout and log back in, now as the all powerful dbAdminAnyDatabase!

$ mongo -u username -p password admin
>

Note that you're only authorized to log into the admin database; by default, you log in to the test database, where you're not yet authorized.

> show collections
2014-03-28T15:23:49.094-0400 error: {
	"$err" : "not authorized for query on test.system.namespaces",
	"code" : 13
} at src/mongo/shell/query.js:131
> 

You'd think that dbAdminAnyDatabase would be able to read any data, but they can't. An admin may not need to have access to the data itself. So once you're an admin, you must create users with read/write access. So let's create another user with a role: readWrite.

> use test
> otheruser = { user : "otheruser" , pwd : "asdf" , roles : [ "readWrite" ] } 
> db.createUser(otheruser)
Successfully added user: { "user" : "username", "roles" : [ "userAdminAnyDatabase" ] }
> exit
$ mongo -u otheruser -p asdf test
MongoDB shell version: 2.6.0
connecting to: test
> db.foo.insert( { a : 1 } )
WriteResult({ "nInserted" : 1 })
> db.foo.find()
{ "_id" : ObjectId("5339854baf5ad8121361771e"), "a" : 1 }
> thirduser = { user : "thirduser" , pwd : "asdf" , roles : [ "readWrite" ] }
{ "user" : "thirduser", "pwd" : "asdf", "roles" : [ "readWrite" ] }
> db.createUser(thirduser)
2014-03-31T11:17:53.378-0400 Error: couldn't add user: not authorized on test to execute command { createUser: "thirduser", pwd: "xxx", roles: [ "readWrite" ], digestPassword: false, writeConcern: { w: "majority", wtimeout: 30000.0 } } at src/mongo/shell/db.js:1004
>use admin
switched to db admin
> show collections
2014-03-31T13:09:16.857-0400 error: {
	"$err" : "not authorized for query on admin.system.namespaces",
	"code" : 13
} at src/mongo/shell/query.js:131
>

So we can see here that readWrite permissions are easily created on a per-database basis, they don't extend to other databases, and they don't allow one to create other users. 

Standard Roles:
read
readWrite
dbAdmin - performs administrative operations
userAdmin - can read from / write to the system.users collection
clusterAdmin - gets additional sharding-related operations
readAnyDatabase
readWriteAnyDatabase
userAdminAnyDatabase
dbAdminAnyDatabase

In order to help ensure that an organization adheres to a policy of least privilege, MongoDB 2.6 has introduced Role Management commands, such as createRole, updateRole, dropRole, grantPrivilegesToRole, etc.

You can authenticate yourself in the mongo shell. You can also authenticate in your connection string. If you authenticate, 

mongo -u myUserName -d myDB -p -> prompts password


Sharding

Yesterday, we discussed Replication, which should never be confused with Sharding. Both involve putting your data on multiple machines, but the similarities stop there. Replication was about redundancy. It was about taking your data and constantly copying it, and being ready, at a moment's notice, to have another machine step in to take control. In no way did replication make your system any faster, just safer.

Sharding is about adding more power to your system, more cheaply than you otherwise could. They're a lot more complicated than replica sets, but the hassle is totally worth it if one machine isn't enough to handle your data.

Here's a basic sharded cluster scenario.


When do you want to shard? Because, keep in mind, it's a hassle. In addition to multiple replica sets, there are routers and config servers, and more software to deal with and more network connections that can go wrong. If you've got 10 GB of data, and it's growing slowly, DO NOT SHARD.

That said, there are some good reasons to shard:
First, if you have too much data to hold on a single machine, you're going to want to shard, so that you can distribute it.
Second, if you're paging a lot of data in and out of memory, and you need to distribute your memory across multiple machines, you can shard.
Third, if you're doing a heavy write load, and you need to distribute it to multiple machines.

Now, I've drawn the basic picture above of sharding, but that's not all that's involved. We also need config servers to keep track of everything and keep it synchronized.


Now, to keep track of everything, we need config servers. A config server requires a very light process, doesn't require much power in your hardware. I've drawn them off to the side because the app doesn't talk to the config server. Config servers don't store any data, they only store metadata, like: 
Where your mongos's are
What collections you've got
Where your collections reside
Where the chunks are
What data is migrating
things like that

The three config servers all have the same data, but they're NOT a replica set. Nevertheless, we do have 3 of them (no more, no less)

We do this because :
If an app needed to talk to a config server, it would create a single point of failure, and we don't want that
Config servers don't scale. If the app were hitting them, there could potentially be a massive load and you'd need a lot of power.

The only time you do need to load your config servers is when you need to pull their cache. 

OK, back to the general operation of the sharded cluster.

Here's the data flow (start drawing two-way arrows): 
App talks to the router, says "I want to read/write data". Router sends it to/from the shard where it belongs, response goes back to the mongos, which sends it back to the app.

There is ONE very very very important consideration in Sharding. This is actually the one time that we enforce a schema. The data you send to the shards MUST contain your shard key. It's very worthwhile to make a good choice, and to take all the time you need to make the right choice, even potentially changing your schema to make it work with the shard key. 

Chunk and Chunk Migration

Let's take an example. Suppose that you have an initial setup with no data at all. We only have 1 sharded cluster, like we've drawn. So, let's give the documents names, and we'll make "name" the shard key. Assume each chunk can hold up to 3 documents before it splits. In reality, it will probably be a lot more, but we want something simple we can understand.

The default situation will put a shard key on shard 1, with a range of minKey to maxKey -- think of those as - infinity to +infinity. There are no chunks on shard 2.

Start adding documents to one shard. One document ( { name: "Alice" } ), no split. Two documents ( { name: "Bob"), no split. Three documents ("Yvonne"), no split. But then at four ("Zoe"), it splits, the one chunk becomes two, a chunk migrates, and now we've got 1 chunk on each, and the rules of which piece of data goes where changes. 

So let's look at what happens in more details. 

First, the data is coming in to the mongos, a router, so it routes the data to the appropriate shard (and chunk). Initially, anything will go to Shard 1 (chunk 1). Both chunks were initially empty, but chunk 1 started filling up.


Next, when chunk 1 got too big, we got a split. During a split, no data goes anywhere, nothing is placed into the files on the mongod's, nothing happens, except the mongos's log this chunk split, and note the demarkation point (Yvette), and communicate that to the config servers. So, chunk 1 now has a range (minKey - Yvette, exclusive) and chunk 2 has a range (Yvette, inclusive - maxKey). So chunk 1 has "Alice" and "Bob", and chunk 2, also on shard 1 has "Yvonne" and "Zoe". Shard 1 and shard 2 are totally naive to these chunks, by the way, but the mongos's and the config servers are totally aware of what's going on.

Next, we have a migration.

During a migration, only ONE chunk is migrated at a time. If you have a big system that's very out-of-balance (and especially if it's under load), this can take awhile. 

First a mongos decides we're imbalanced (2 on one shard, 0 on the other). It notifies the mongod's that it's migrating a chunk, and in doing so, locks all other mongos's out of migration. When the initiating mongos gets permission, it tells the source and destination shards to start migrating data. During this migration, all reads & writes go to the first shard. Updates and inserts on the chunk are communicated to the second shard, and when everything is done, the mongos notifies the config servers, a two-phase commit occurs, and, from a bookkeeping perspective, the chunk is now on shard 2 (even though both shards have a copy). At this point, all reads & writes will go to shard 2, and eventually the data on shard 1 will get deleted. 

Remember, a chunk is migrated only when the shard with the most chunks has at least 2 more chunks than the shard with the fewest.

It is migrated from the shard with the most, to the shard with the least.


Config Servers:
Just to remind you with Config servers:

First, they're NOT a replica set. 3 standalone servers that each can handle things independently.

Second, When a migration will happen, first an OK must come from each of the 3 config servers.

Now, what happens when a shard is added?
It's treated, instantly, like any other shard, only it's empty. So, next chance for a migration, it will be grabbing chunks.
Can you delete shards?
Absolutely! You just have to move its chunks away, then remove the shard. 
Chunks
NOT files. Just logical ranges that we keep track of.
The only thing that knows what a chunk is, is the config server.


Shard Key Selection
Try to figure out the most common query. For instance, an email program. 
{ _id: "XXXX"
to: "XXXX"
from: "XXXX"
subject: "XXXX"
body:"XXXX"
timestamp:"XXXX"
attn: "XXXX"
user: "XXXX"
}

What is the most common query we'll see? It's one you don't even think about. It happens as you enter your inbox:  Inbox loading. db.email.find().sort({timestamp: -1})


So, we're always sorting by timestamp, and a shard key needs an index. should we shard on timestamp?
NO!!!
Why?
No write scaling: As we add emails, chunks are split, and one chunk has everything up to maxKey. This chunk will get ALL of the writes, and it's necessarily on just one server.


BUT there are some advantages to time. For instance, finding just RECENT emails would be quite performant. Even so, it's probably not worth it since the writes are so bad.

Solution? Hash it!!

This will distribute the writes. 

Disadvantages?
Well, unfortunately, you can't do ranges easily for hashes. Instead queries will be scatter-gather.

Something to think about for a shard key: Cardinality

You can't split when the shard key is the SAME for everything in a chunk. This can easily happen if one shard key value will get much more than 64 MB. And large chunks are still just 1 chunk each. So a large chunk will be held by only one server, and will count for only one chunk.

This could easily happen if you shard on sender's email. 

Solution?

Compound shard key!
For instance, ({username, date})
This will allow you to break up chunks appropriately
Tags
Allows you to distribute chunks preferentially. This is most useful if you want certain data to be in certain locations, for instance, if your data centers and your customers are distributed.

Imagine we've got users & data centers in each of 3 countries. For example,  the US, the UK, Japan

We have users in each country. Latency is a problem across regions. So, we set rules according to the shard key.

Shard key: Region + Username

We can create tag ranges. 

minKey - Japan (Japan)

Japan - UK (UK)

UK - maxKey

Setting up a sharded cluster

(lunch, day 3)

Backups
They're pretty straightforward in most cases, but they get tricky for a sharded cluster.

For a sharded system:
1. Stop the balancer
2. Backup config
3. Backup individual shards (snapshots, mongodump, etc.)
Fsync lock
Typically by running it on a scondary on each one.
Fsync unlock
4. Restart the balancer

This will avoid causing problems, and allow you to do backups hot.


Authentication and Access Controls

I'm just going to be talking about the basics of Authentication and access controls.

SHOW
use admin
db.addUser( { username: "Will", pwd: "MongoDB", roles: [ "dbAdminAnyDatabase" , "readWriteAnyDatabase" , "userAdminAnyDatabase" , "clusterAdminAnyDatabase" ] } )

A list of roles can be found here:  
http://docs.mongodb.org/manual/reference/privilege-documents/
When a password is created, the password is hashed automatically.
SHOW
show collections
Error! I didn't log in!
db.auth( "Will" , "MongoDB" ) 
Now I have access.
db.addUser( { username: "Oz" , pwd : "MongoDB" , roles : [ "read" ] } )

Obviously, you'd do this in a driver, it would take your password, hash it, you'd be good.

Later versions will handle a lot of this for you, and allow you to set up groups of users.


Production Deployments of MongoDB

SHOW
http://docs.mongodb.org/manual/administration/production-notes/

Most people who call in and complain have missed doing something important that is mentioned on this page.

It's a GREAT checklist, with everything from your hardware/software to your MongoDB implementations, filesystem versions, etc.

Monitoring (BUILD THIS)



Mongostat, Mongotop, Load Server (BUILD THIS)

db.stats()/db.collection.stats(), Profiler
db.killOp and db.currentOp (NEEDS WORK)

db.serverStatus() -- show them even though it's kind of useless, except currentConnections. Really, you have to sample it. Most useful if you do it a couple of times & look @ deltas. 

MongoDB Monitoring Service
MAKE SURE YOU NEVER DISPLAY CUSTOMER INFO. 

If you have it, just have a demo account. (30 minutes)
alerts
on prem

MMS Monitoring 

NOTE TO INSTRUCTOR: For this lesson and the following one, it is a good idea to have MMS Monitoring and backup setup in advance, get it running with some data to show the students.

Objective: Students will understand the advantages of using the MMS Monitoring Service, and will understand where to go in order to set it up.

MMS is the MongoDB Management Service. It will provide you with free monitoring, and with backup for a fee (though there is a free tier). It involves running a lightweight monitoring agent in the background on a machine with access to your servers (it could easily be on one or more of your servers), which can then monitor the servers in the cluster and report back time-series statistics that are likely to be interesting.

In order to sign up for it, just go to mms.mongodb.com - all you need is an email. Once you've got it set up and running on a server, you will begin to collect statistics. You can display them at as granular a level as you like. You can look at your query load, your lock percentages, your page faults or background flush times, basically a lot of things that make it easy for you to see when something goes wrong with your system -- or better yet, when something is about to go wrong, and you still have time to fix it.

You can see that we've set up a dashboard that allows you to set up the granularity and zoom level of your data. You can click between hosts, control when you get alerts, assign other users with various permission levels -- whatever you like. 

You can set this up for a standalone server, for a replica set, or for a sharded cluster. The MMS agent doesn't collect any data on your system, just metadata about the server, but if you're concerned, you can set up an on-premises version of MMS with a MongoDB subscription. 


MMS Backup (In Progress)
MMS, the MongoDB Management Service, also provides a backup service. Like MMS Monitoring, it is available through us, or using an on-premises version with a standard subscription to MongoDB. 

MMS Backup uses different agent than MMS Monitoring. The MMS backup agent also doesn't just upload metadata from your system, it uploads the data. It provides about as much load on your system as having a secondary, or an extra secondary. 





GridFS lesson (optional) (TO DO)

Appendix
Things to do
Finish MongoDB History

