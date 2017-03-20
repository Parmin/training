.. This includes the page title and the MongoDB graphics:
.. include:: header.tmpl


Agenda
------

Introduction
~~~~~~~~~~~~

Advanced Administrator Training is designed for operations staff responsible for
maintaining MongoDB applications. The instructor leads teams through a series
of scenarios that represent potential issues encountered during the normal
operation of MongoDB. Teams are hands-on throughout the course, actively
working together to identify and implement solutions. The instructor evaluates
teams based on the speed, elegance, and effectiveness of their solutions and
provides feedback on strategy and best practices.

Each scenario exercises and develops skills in critical areas such as
diagnostics, troubleshooting, maintenance, performance tuning, and disaster
recovery. Each team will be provided with their own Amazon EC2 machines to work
with. The instructor will supply IP addresses. The scenarios for this training
fall into four subject areas as follows.

Backups and Recovery
~~~~~~~~~~~~~~~~~~~~

If you use a backup service like MMS Backup, then most of the time you don’t
have to worry about backup.  But when something breaks your production data, it
can require some manual care to repair it.  In this section, students work
through an extended exercise restoring a single collection to a previous point
in time.

Replication
~~~~~~~~~~~

Most production deployments of MongoDB should use replica sets, which provide
automatic failover.  In this section you’ll learn to do the following with
minimal downtime:

    * Roll out upgrades (with a single failover)
    * Roll out performance fixes (with a single failover)
    * Diagnose and fix a downed node (with no downtime)

Diagnostics
~~~~~~~~~~~

The scenarios in this section will develop familiarity with:

    * The MongoDB profiler
    * Using profiling data to find slow operations
    * Writing aggregation queries for reporting and diagnostics

Sharding and Performance Troubleshooting
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this section students learn to diagnose and fix a wide variety of issues
that may arise in a sharded cluster:

    * rogue queries  (a single query that monopolizes the system)
    * poorly optimized queries  (application queries that can be improved)
    * missing indexes
    * bad default OS settings
