================
NHTT Labs - Will
================

Indexing Quiz Questions
-----------------------

url here (to take quiz): https://www.research.net/r/XGDFBJQ
to edit: https://www.surveymonkey.com/summary/7pFpOSfaY9uUMCZUDj2wOcgRWwBI4Mg9GNnjmSRp6ljAHTZZkWRRMM2hqSPg5sMP

Create indexes that are optimized for the following queries. 

If there is more than one query, assume that all are common and create a set of
indices that will work for all of them.

1.

.. code-block:: 

  db.users.find( { username : <string> } )
  db.users.find( { isActive : true, username: <string> } )

2. 

.. code-block:: javascript

  db.zips.find( { city : { $in : [ <string>, <string>, <string> ] },
                  state : <string> } ).sort( { zip_code : 1 } )

3. 

.. code-block:: javascript

  db.accounts.updateMany( { lastLogin : { $gte : ISODate( "2016-10-01" ) },
                            isActive : true },
                          { $inc : { balanceDue : NumberDecimal(10.00) } } )

4. 

.. code-block:: javascript

  db.people.insertOne( { username : "will@mongodb.com", password : "12345",
                         employer : "MongoDB" } )


5.

.. code-block:: javascript

  db.users.find( { isActive : true } ).sort( { lastLogin : -1, lastName : 1,
                                               firstName : 1 } )

6.

.. code-block:: javascript

  db.accounts.find( { accountBalance : { $gte : NumberDecimal(100000.00) } },
                      city: "New York" ).sort( { lastName: 1, firstName: 1 } )



Index Quiz Answers
------------------

1.

.. code-block:: javascript

  { username : 1, isActive : 1 }

Descending is OK, too.

This has to be the ordering, however, because if it were { isActive : 1,
username : 1 }, then the index couldn't be used for the first query.

An alternative might be two indexes:

.. code-block:: javascript

  { username : 1 }
  { isActive : 1, username : 1 }, { partialFilterExpression : { isActive : true } }

but the overhead of maintaining two indexes might not be worth it.


2.

Any of the following:

.. code-block:: javascript

  { state : 1, zip_code: 1, city : 1 }
  { state : 1, zip_code: 1, city : -1 }
  { state : 1, zip_code: -1, city : 1 }
  { state : 1, zip_code: -1, city : -1 }
  { state : -1, zip_code: 1, city : 1 }
  { state : -1, zip_code: 1, city : -1 }
  { state : -1, zip_code: -1, city : 1 }
  { state : -1, zip_code: -1, city : -1 }

Descending is OK too, in any or all of the fields.

The order, however, is important. State needs to come first in order to
efficiently use the index, and zip_code needs to come second in order to use
the index for the sort.

3. 

any of the following:

.. code-block:: javascript

  { isActive : 1, lastLogin : 1 } 
  { isActive : 1, lastLogin : -1 } 
  { isActive : -1, lastLogin : 1 } 
  { isActive : -1, lastLogin : -1 } 

4. 

No index is required for this. Insertions don't benefit from indexes, and are actually slowed down by them.

5. 

Any of the following will work:

.. code-block:: javascript

  { isActive : 1, lastLogin : -1, lastName: 1, firstName: 1 }
  { isActive : -1, lastLogin : -1, lastName: 1, firstName: 1 }
  { isActive : 1, lastLogin : 1, lastName: -1, firstName: -1 }
  { isActive : -1, lastLogin : 1, lastName: -1, firstName: -1 }


6. { city: 1, lastName: 1, firstName: 1, accountBalance: 1 }
   (order doesn't matter, except that lastName and firstName must be aligned).


Internals and Storage Engines
-----------------------------

1. Determine the truth of the following statement: Updating a non-indexed field in a document in a collection can lead to updates of indexes for that collection.

:choices:
   :yes: True for MMAPv1, but false for WiredTiger
   :no: False for MMAPv1, but true for WiredTiger
   :no: False for both MMAPv1 and WiredTiger
   :no: True for both MMAPv1 and WiredTiger

2. Which of the following features can be affected by your choice of storage engine?

   :yes: On-disk encryption
   :yes: On-disk compression
   :yes: Capped collection implementation
   :yes: Locking granularity
   :no: Ability to safely run without journaling
   :yes: Data files
   :yes: Ability to utilize multicore processors in parallel
   :yes: Layout of data files

3. For the WiredTiger cache, which of the following represent the differences between on-disk pages and pages in the cache?

   :yes: Presence of a page-specific index
   :yes: Compression and encryption
   :yes: Update list
   :no: Ordering of documents (for a clean page)

4. For WiredTiger, what are the differences between collections and indexes?
   
   :no: Indexes are stored in btrees, but collections are stored in flat data structures
   :yes: There is (almost) no difference between indexes and collections
   :yes: An index is (usually) smaller than a collection 
   :no: 


Replication
-----------



Schema Design
-------------

* Draw them from the available options.


