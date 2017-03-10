Objective
+++++++++

The objective in these exercises is to put in practice as many of the
aggregation framework operators as possible. There are extension
exercises for savvy developers to be challenged further and as time
permits.

Premise
+++++++

.. include:: student-agg.rst
   :start-after: start-premise
   :end-before: end-premise

Prerequisites
+++++++++++++

- Run the ``~/scripts/Aggregation/premise-1-2.sh`` script which will set up an
  empty 3 node replica set.

.. include:: newpage.tmpl

Setup
+++++

Each student should perform the following operations:

.. include:: student-agg.rst
   :start-after: start-setup
   :end-before: end-setup

Exercise 1
++++++++++

.. include:: student-agg.rst
   :start-after: start-exercise-one
   :end-before: end-exercise-one

.. include:: newpage.tmpl

Solution 1
++++++++++

::

  // response time by operation type
  db.system.profile.aggregate( { $group : {
  _id :"$op",
  count:{$sum:1},
  "max response time":{$max:"$millis"}, "avg response time":{$avg:"$millis"}
  }});

Result ::

  {
    "result" : [
      {
        "_id" : "update",
        "count" : 100,
        "max response time" : 0,
        "avg response time" : 0
      },
      {
        "_id" : "query",
        "count" : 100,
        "max response time" : 32,
        "avg response time" : 26.29
      },
      {
        "_id" : "insert",
        "count" : 3903,
        "max response time" : 3,
        "avg response time" : 0.0007686395080707148
      }
    ],
    "ok" : 1
  }

.. include:: newpage.tmpl

Exercise 2
++++++++++

.. include:: student-agg.rst
   :start-after: start-exercise-two
   :end-before: end-exercise-two

.. include:: newpage.tmpl

Solution 2
++++++++++

::

  // response time analysis
  db.system.profile.aggregate(
    [
      { $project :
        {
          "op" : "$op",
          "millis" : "$millis",
          "timeAcquiringMicrosrMS" : { $divide : [ "$lockStats.timeAcquiringMicros.r", 1000 ] },
          "timeAcquiringMicroswMS" : { $divide : [ "$lockStats.timeAcquiringMicros.w", 1000 ] },
          "timeLockedMicrosrMS" : { $divide : [ "$lockStats.timeLockedMicros.r", 1000 ] },
          "timeLockedMicroswMS" : { $divide : [ "$lockStats.timeLockedMicros.w", 1000 ] }
        }
      },
      { $project :
        {
          "op" : "$op",
          "millis" : "$millis",
          "total_time" : { $add : [ "$millis", "$timeAcquiringMicrosrMS", "$timeAcquiringMicroswMS" ] },
          "timeAcquiringMicrosrMS" : "$timeAcquiringMicrosrMS",
          "timeAcquiringMicroswMS" : "$timeAcquiringMicroswMS",
          "timeLockedMicrosrMS" : "$timeLockedMicrosrMS",
          "timeLockedMicroswMS" : "$timeLockedMicroswMS"
        }
      },
      { $group :
        {
          _id : "$op",
          "average response time" : { $avg : "$millis" },
          "average response time + acquire time": { $avg: "$total_time"},
          "average acquire time reads" : { $avg : "$timeAcquiringMicrosrMS" },
          "average acquire time writes" : { $avg : "$timeAcquiringMicroswMS" },
          "average lock time reads" : { $avg : "$timeLockedMicrosrMS" },
          "average lock time writes" : { $avg : "$timeLockedMicroswMS" }
        }
      }
    ]
  );

.. include:: newpage.tmpl

Result ::

    {
    "result" : [
      {
        "_id" : "command",
        "average response time" : 20,
        "average response time + acquire time" : 20.006,
        "average acquire time reads" : 0.004,
        "average acquire time writes" : 0.002,
        "average lock time reads" : 20.813,
        "average lock time writes" : 0
      },
      {
        "_id" : "update",
        "average response time" : 0,
        "average response time + acquire time" : 0.0023000000000000017,
        "average acquire time reads" : 0,
        "average acquire time writes" : 0.0023000000000000017,
        "average lock time reads" : 0,
        "average lock time writes" : 0.07200000000000001
      },
      {
        "_id" : "query",
        "average response time" : 26.29,
        "average response time + acquire time" : 27.072920000000003,
        "average acquire time reads" : 0.6860699999999995,
        "average acquire time writes" : 0.09685000000000009,
        "average lock time reads" : 27.512089999999997,
        "average lock time writes" : 0
      },
      {
        "_id" : "insert",
        "average response time" : 0.0007690335811330429,
        "average response time + acquire time" : 0.006153806716226541,
        "average acquire time reads" : 0,
        "average acquire time writes" : 0.005384773135093499,
        "average lock time reads" : 0,
        "average lock time writes" : 0.009285824147654708
      }
    ],
    "ok" : 1
  }
