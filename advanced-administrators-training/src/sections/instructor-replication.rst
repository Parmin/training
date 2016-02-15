Premise 1
+++++++++

.. include:: student-replication.rst
   :start-after: start-premise-one
   :end-before: end-premise-one

Setup
+++++

- Use the same VM from the backup/restore exercise. This is preloaded with
  versions 2.4 and 2.6 of MongoDB.
- Make sure you have done the "Cleanup" step of the previous exercise,
  to remove everything from MMS.
- Run ``~/scripts/Replication/premise-1-2.sh``
- This script will create a 3 node replica set running the previous MongoDB
  version release with data in the ``test`` database in the ``users`` directory.
  Provide one replica set per team.

Solution 1
++++++++++

1. Take a secondary offline; restart it with the new binary.
2. Take the other secondary (if there is one) offline, and restart it with the new
   binary as well.
3. Perform an ``rs.stepDown()`` on the primary.  This will force the primary to step
   down gracefully and attempt to avoid election as primary for 60 seconds (may
   need to increase this time by specifying it as a parameter to rs.stepDown() if
   this node is configured with a higher priority, so that it doesn't try to become
   primary again until it is restarted with the new binary). Restart it with the new binary.

Now your replica set should be fully upgraded with minimal downtime from an
application perspective (i.e. just a replica set failover).

Premise 2
+++++++++

.. include:: student-replication.rst
   :start-after: start-premise-two
   :end-before: end-premise-two

Setup
+++++

- Use the same VM from the backup/restore exercise. This is preloaded with
  versions 2.4 and 2.6 of MongoDB.
- Run ``~/scripts/Replication/premise-1-2.sh``
- This script will create a 3 node replica set running the previous MongoDB
  version release with data in the ``test`` database in the ``users`` directory.
  Provide one replica set per team.

Solution 2
++++++++++

A rolling index build. Similar to the upgrade process, the solution is as follows:

1. For each secondary in the set, build an index according to the following steps:
     1. Restart the ``mongod`` without the ``--replSet`` option and on a different port.
     2. Create the index using ``ensureIndex()``.
     3. Restart the ``mongod`` as a member of the replica set on its usual port
2. Perform an ``rs.stepDown()`` on the current primary and make sure to wait for
   one of the other nodes to be elected primary.
3. Build the index on the former primary using the same procedure as above.

Ensure that the oplog window is large enough to permit the indexing to complete
without the node falling too far behind to catch up when it is re-introduced into
the replica set.

Premise 1 with MMS Automation
++++++++++++++++++++++++++++++++++++

.. include:: student-replication.rst
   :start-after: start-premises-one-and-two-with-mms-automation
   :end-before: end-premises-one-and-two-with-mms-automation

Setup
+++++

- Use the same VM from the previous exercises
- Re-run ``~/scripts/Replication/premise-1-2.sh``

Solution 1 with MMS Automation
++++++++++++++++++++++++++++++++++++

First import the cluster into MMS.

1. Add > Import Existing for Monitoring

    - for "Host Type" choose "Replica Set"
    - for "Internal Hostname" paste the output of ``hostname`` on the VM
    - for "Port" specify 27017

   MMS should discover the whole replica set once you add the primary.

2. Add > Import Existing for Automation

    - choose the replica set from the "Deployment Item" dropdown

Then use Automation to perform a rolling upgrade.

1. Click the wrench next to the replica set to edit the replica set

2. Change the "version" dropdown to the latest 2.6.x

3. Click "Review and deploy"


Premise 3
+++++++++

.. include:: student-replication.rst
   :start-after: start-premise-three
   :end-before: end-premise-three

Setup
+++++

- Use the same VM from the backup/restore exercise. This is preloaded with
  versions 2.4 and 2.6 of MongoDB.
- Run ``~/scripts/Replication/premise-3.sh`` which will bring up a replica
  set, with a member with a small oplog, and insert enough data until it falls
  off the oplog.

Note that the RS102 error message in the system log indicates the "fall off" issue.

Solution 3
++++++++++

1. Take the node down
2. Delete the data files
3. Restart the node
4. Wait for full resync

Points for elegance if they resize the oplog to something bigger or change it
back to the default.
