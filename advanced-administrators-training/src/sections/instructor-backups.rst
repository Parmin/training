.. this just has the premise section.

.. include:: student-backups.rst


Setup
+++++

To set up this scenario, ssh into each instance and run the following script::

  ~/scripts/Backups/premise-1.sh

This script will confirm that the automation agent is running and start a
replica set on ports 27017, 27018, 27019. Then it will prompt you to import the
replica set into MMS.

1. Log in to MMS as ``advanced-ops+instructor@mongodb.com``

2. Choose the MMS Group ``team01-advanced-ops`` from the dropdown in the top-left

3. Install the Monitoring and Backup agents

   * see https://docs.mms.mongodb.com/tutorial/move-agent-to-new-server/#install-additional-agent-as-hot-standby-for-high-availability

4. Import Team 1's replica set for monitoring

   * see https://docs.mms.mongodb.com/tutorial/add-hosts-to-monitoring/#add-mongodb-processes

5. Activate Backup for Team 1's replica set

   * see https://docs.mms.mongodb.com/tutorial/enable-backup-for-replica-set/#procedure

6. Repeat steps 2-5 for each team

7. Re-run the script for on each EC2 instance

   * This will confirm that Backup is enabled on the replica set and finish setting up the scenario.

Cleanup
+++++++

Once students are done with this exercise, terminate Backup for all the replica sets and remove the
replica sets from MMS.

Solution
++++++++

Obtain the backup
*****************

1. Connect to the server using the ``mongo`` shell and find the bad operation in
   the oplog::

     mongo
     use local
     var badOp = db.oplog.rs.find({ op: "c" }).sort({ ts: -1 }).next();

2. Find the timestamp of the most recent good operation::

     db.oplog.rs.find({ ts: { $lt: badOp.ts } }).sort({ ts: -1 }).next()
    
3. In the MMS console, go to "Backup", your group's replica set, "Restore", "Use
   Exact Oplog Timestamp", and enter the two numeric values from the
   ``Timestamp`` value you found in the oplog.

4. Choose "Pull via Secure HTTP" and ``curl`` the download URL from the ec2
   instance. Keep this tar file; you'll need to unpack it several times while
   restoring.

Restore the backup
******************

This is a many-step process; see

https://docs.mms.mongodb.com/tutorial/restore-replica-set/#restore-the-primary
