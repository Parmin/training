NHTT Labs - Will
================

Indexing Quiz Questions
-----------------------

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

  db.people.updateMany( { lastLogin : { $lte : ISODate( "2016-01-01" ) },
                          isActive : true },
                        { $set : { isActive : false } } )

6.

.. code-block:: javascript

  db.users.find( { isActive : true } ).sort( { lastLogin : -1, lastName : 1,
                                               firstName : 1 } )




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

Any of the following:

.. code-block:: javascript

  { isActive : 1, lastLogin : 1 } 
  { isActive : 1, lastLogin : -1 } 
  { isActive : -1, lastLogin : 1 } 
  { isActive : -1, lastLogin : -1 } 

This is the ordering that will allow for efficient index usage.

6. 

Any of the following will work:

.. code-block:: javascript

  { isActive : 1, lastLogin : -1, lastName: 1, firstName: 1 }
  { isActive : -1, lastLogin : -1, lastName: 1, firstName: 1 }
  { isActive : 1, lastLogin : 1, lastName: -1, firstName: -1 }
  { isActive : -1, lastLogin : 1, lastName: -1, firstName: -1 }




Internals and Storage Engines
-----------------------------


Replication
-----------



Schema Design
-------------

* Draw them from the available options.


