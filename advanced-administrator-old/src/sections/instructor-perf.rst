
Premise 1
+++++++++

.. include:: student-perf.rst
   :start-after: start-premise-one
   :end-before: end-premise-one

Solution 1
++++++++++

Find the op using ``db.CurrentOp``. And then end it with ``db.killOp()``.


Instances
+++++++++

For the next exercise you will use the clusters launched by `shard.sh`

Each cluster is made up of 2 shards with 3-nodes replica set per shard,
1 config server node and 1 mongos node.  Each element of the cluster
resides on its own EC2 instance so 8 machines in total.

The cluster is configured badly:

* Data is missing indexes

* They each have low ulimits

* They have a high readahead set

* They are mounted with atime

* EXT3 File System

* EBS volume



Premise 2
+++++++++

.. include:: student-perf.rst
   :start-after: start-premise-two
   :end-before: end-premise-two

Solution 2
++++++++++

Turn down readahead, mount with noatime, raise ulimits, make sure all queries
are using appropriate indexes, change the filesystem, and come up with a better
alternative for a shard key given the sample queries and the data set.

Query solutions:

- finding users by screen name - missing an index::

    Q. db.live.find( { "user.screen_name" : "____thaaly" } )
    A. db.live.ensureIndex( { "user.screen_name" : 1 } )

- finding all users who have a particular name e.g. Beatriz - regex not anchored at the start of the string so won't use an index efficiently (index scan)::

    Q. db.live.find( { "user.name" : /Beatriz/ } )
    A. db.live.find( { "user.name" : /^Beatriz/ } )

- finding all users in the Brasilia timezone with more than 70 friends, and sorting by most friends -
  only using one index and not a compound, and sorting by non-indexed field::

    Q. db.live.find( { "user.time_zone" : "Brasilia",
                       "user.friends_count" : { $gt : 70 } } )
                .sort( { "user.friends_count" : -1 } )
    A. db.live.ensureIndex( { "user.time_zone" : 1, "user.friends_count" : 1 } )
