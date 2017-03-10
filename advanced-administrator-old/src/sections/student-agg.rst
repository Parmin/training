Objective
+++++++++

The objective of these exercises is practice as many of the
aggregation framework operators as possible.

Premise
+++++++

.. start-premise

*Your cluster is experiencing some performance issues and you would
like to determine where the bottlenecks are. You will need to create
statistics on slow queries, locking, and operations: use the database
profiler and write some aggregation queries to analyze the profiling data.*

.. end-premise

.. start-setup

1. To prepare the system, first enable the profiler for a new agg
   database (to record all queries): ::

      > use agg;
      > db.setProfilingLevel(2);

2. Add some sample data: ::

      > for (i=0; i<100000; i++) { db.wargame.insert( { count : i } ); }

3. Add some queries: ::

      > for (i=0; i<100; i++) { db.wargame.find( { count : i } ).toArray(); }
      > for (i=0; i<100; i++) { db.wargame.update( { count : i },
                                                   { $set : { "another_field" : i } } ); }

.. end-setup

Exercise 1
++++++++++

.. start-exercise-one

Find the maximum response time and average response time for each type of
operation in the ``system.profile`` collection. Hint: group on the "``op``" field.

Your result should have the following form: ::

   {
           "result" : [
                   {
                           "_id" : "update",
                           "count" : <NUMBER>,
                           "max response time" : <NUMBER>,
                           "avg response time" : <NUMBER>
                   },
                   {
                           "_id" : "query",
                           "count" : <NUMBER>,
                           "max response time" : <NUMBER>,
                           "avg response time" : <NUMBER>
                   },
                   {
                           "_id" : "insert",
                           "count" : <NUMBER>,
                           "max response time" : <NUMBER>,
                           "avg response time" : <NUMBER>
                   }

                   ... for every operation in the system.profile.op field
           ],
           "ok" : 1
   }

.. end-exercise-one

.. include:: newpage.tmpl

Exercise 2
++++++++++

.. start-exercise-two

Render detailed statistics using the data from the ``system.profile`` collection.

Your result should have the following form: ::

   {
           "result" : [
                   {
                           "_id" : "command",
                           "average response time" : <NUMBER>,
                           "average response time + acquire time" : <NUMBER>,
                           "average acquire time reads" : <NUMBER>,
                           "average acquire time writes" : <NUMBER>,
                           "average lock time reads" : <NUMBER>,
                           "average lock time writes" : <NUMBER>
                   },
                   {
                           "_id" : "update",
                           "average response time" : <NUMBER>,
                           "average response time + acquire time" : <NUMBER>,
                           "average acquire time reads" : <NUMBER>,
                           "average acquire time writes" : <NUMBER>,
                           "average lock time reads" : <NUMBER>,
                           "average lock time writes" : <NUMBER>
                   },
                   {
                           "_id" : "query",
                           "average response time" : <NUMBER>,
                           "average response time + acquire time" : <NUMBER>,
                           "average acquire time reads" : <NUMBER>,
                           "average acquire time writes" : <NUMBER>,
                           "average lock time reads" : <NUMBER>,
                           "average lock time writes" : <NUMBER>
                   },
                   {
                           "_id" : "insert",
                           "average response time" : <NUMBER>,
                           "average response time + acquire time" : <NUMBER>,
                           "average acquire time reads" : <NUMBER>,
                           "average acquire time writes" : <NUMBER>,
                           "average lock time reads" : <NUMBER>,
                           "average lock time writes" : <NUMBER>
                   }

                   ... for every operation in the system.profile.op field

           ],
           "ok" : 1
   }

.. end-exercise-two
