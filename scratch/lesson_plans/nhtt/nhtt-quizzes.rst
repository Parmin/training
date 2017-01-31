================
NHTT Labs - Will
================

Indexing Quiz Questions
-----------------------

The Quiz is in SurveyMonkey:
- url to take quiz: https://www.research.net/r/XGDFBJQ
- url to edit quiz: https://www.surveymonkey.com/summary/7pFpOSfaY9uUMCZUDj2wOcgRWwBI4Mg9GNnjmSRp6ljAHTZZkWRRMM2hqSPg5sMP


Create indexes that are optimized for the following queries.

If there is more than one query, assume that all are common and create a set of
indices that will work for all of them.

Note that the order of the questions is different for all people.

Some comments on this quiz:
- may want to not shuffle the questions
- we need a different dataset to explain equality/sort/range. It would be good to have 1-N relationships for each level (not a 1-1 like city to zipcode)
- let's not use boolean fields, unless the purpose is to show low cardinality

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



/poll "Which of the following features can be affected by your choice of storage engine?"  "On-disk encryption" "On-disk compression" "Capped collection implementation" "Locking granularity" "Ability to safely run without journaling" "Data files" "Ability to utilize multicore processors in parallel"

/poll "For the WiredTiger cache, which of the following represent the differences between on-disk pages and pages in the cache?" "Presence of a page-specific index" "Compression and encryption" "Update list" "Ordering of documents (for a clean page)"

/poll "For WiredTiger, what are the differences between collections and indexes?" "Indexes are stored in btrees, but collections are stored in flat data structures" "There is (almost) no difference between indexes and collections" "An index is (usually) smaller than a collection "


Replication
-----------

  /poll   "When can you use secondaries for scaling?" "When you have a special use case that needs special indexes" "When you want to colocate a server and the application" "When you are OK with stale data" "When your primary cannot handle the read load"

/poll "How are oplog entries communicated from the primary to the secondaries?" "They are pushed to the secondaries" "They are pulled from the primary" "They are pulled from the config servers" "This is decided by arbiters"

/poll "When is idempotence important in the oplog?" "During the initial sync" "At all times when pulling the oplog" "When there are multiple servers pushing oplog entries"

/poll "When is an election called?" "When there is no primary" "When no other server has called for an election" "When a write comes in" "When oplog entries must be replicated"



Why must there be an odd number of members in a replica set?


Schema Design
-------------

* Draw them from the available options.
