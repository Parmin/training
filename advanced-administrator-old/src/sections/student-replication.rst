Premise 1
+++++++++

.. start-premise-one

"*MongoDB releases a new version. How do we upgrade our production
systems with minimal downtime?*"

.. end-premise-one

Premise 2
+++++++++

.. start-premise-two

"*We have a new set of queries we want to run against the production
system.  But whenever we try to build the indexes for these queries,
we experience a massive slowdown. How can we build indexes on the
production system while minimizing the performance penalty?*"

You will build indexes on the ``test.users`` collection for the fields
``emailAddress`` and ``userId``.

.. end-premise-two

Premise 1 with MMS Automation
++++++++++++++++++++++++++++++++++++

.. note: once MMS Automation supports rolling index builds, students can redo
         premise 2 as well

.. start-premises-one-and-two-with-mms-automation

Try Premise 1 again, but using MMS Automation.
First the instructor will reset your replica set to its original state.  Then
you can import the replica set into MMS and use Automation to perform a
minimal-downtime version upgrade.

.. end-premises-one-and-two-with-mms-automation

Premise 3
+++++++++

.. start-premise-three

"*Your primary has become unavailable because of a power
surge. Fortunately, automatic failover kicked in and the system never
went down. Unfortunately, you never set alerts to inform you when a
node becomes unavailable, so weeks go by until you notice.  When you
bring it back up, the node does not restart cleanly. Find out why and
fix it.*"

.. end-premise-three
