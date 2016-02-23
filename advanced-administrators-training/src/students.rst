.. This includes the page title and the MongoDB graphics:
.. include:: header.tmpl


Introduction
~~~~~~~~~~~~

Advanced Administrator Training is a 2-day on-site course designed for DBAs. The instructor leads teams through a series of scenarios that represent potential issues encountered during the normal operation of MongoDB. Teams are hands-on throughout the course, actively working together to identify and implement solutions. The instructor evaluates teams based on the speed, elegance, and effectiveness of their solutions and provides feedback on strategy and best practices.


Exercises
~~~~~~~~~

Each scenario exercises and develops skills in critical areas such as diagnostics, troubleshooting, maintenance, performance tuning, and disaster recovery.

Each team will be provided with their own Amazon EC2 machines to work with. The instructor will supply IP addresses.

From the terminal on a Linux/Mac machine, connect with the following command::

  ssh ec2-xx-xxx-xx-xx.compute-1.amazonaws.com \
      -l ec2-user -i /path/to/AdvancedOpsTraining.pem

When connecting from a Windows machine, ensure there is a suitable SSH
client installed that can handle file authentication, such as *PuTTY*
and *PuTTYgen*. Refer to the linked instructions for `using PEM files with PuTTY
<http://support.cdh.ucla.edu/help/132-file-transfer-protocol-ftp/583-converting-your-private-key->`_
[#url-for-putty]_.

Users should log in as ``ec2-user``, which has ``sudo`` access.
Each team will have their own instance to connect to in order to complete each exercise.

The instructor will also have SSH access to all the instances in order to run
scripts that set up each scenario.

.. [#url-for-putty] http://support.cdh.ucla.edu/help/132-file-transfer-protocol-ftp/583-converting-your-private-key-

Backups and Recovery
~~~~~~~~~~~~~~~~~~~~

.. include:: sections/student-backups.rst

Replication
~~~~~~~~~~~

.. include:: sections/student-replication.rst

Aggregation Framework + Map-Reduce
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. include:: sections/student-agg.rst

Sharding & Performance Troubleshooting
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. include:: sections/student-perf.rst

Security
~~~~~~~~

.. include:: sections/student-security.rst
