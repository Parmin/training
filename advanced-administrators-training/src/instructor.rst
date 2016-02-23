.. This includes the page title and the MongoDB graphics:
.. include:: header.tmpl

Advanced Administrators' Instructor Material
--------------------------------------------

Introduction
~~~~~~~~~~~~

Advanced Administrators' Training is a 2-day consulting engagement at the customer
site. It consists of splitting the students into teams and running a set of
scenarios on MongoDB that pits each team against each other in a bid to
identify and provide a solution to the problem put in front of them. Teams are
awarded points on speed, elegance, and effectiveness of their solution. The
winning team receives a prize.

Advanced Administrators' Training is an entirely practical set of exercises, where
teams are hands-on throughout the day, actively working together to identify
and implement a solution.

Audience
~~~~~~~~

This session is designed for 4-12 people. Audience should be technical. The day
is mostly beneficial for operations/DBAs, but developers may also find content
interesting.

The Advanced Administrators' Training session should ideally follow on from a
MongoDB training course, as candidates will be using prior knowledge to
complete exercises. This is not designed for complete beginners.

Prerequisites
~~~~~~~~~~~~~

You will need to make sure that there are adequate resources in place in order
to deliver a successful session. You will require:

.. list-table::
   :header-rows: 1
   :widths: 88, 12

   * - **Requirement**
     - **Importance**
   * - An instructor machine (your laptop is OK)
     - CRITICAL
   * - A training room with a projector
     - CRITICAL
   * - 1 machine per team (teams are made up of 3 or 4 people)
     - CRITICAL
   * - Machines should have outside Internet access (both HTTP and SSH
       required), as they will be shelling out to EC2 instances.
     - CRITICAL
   * - A flipchart/whiteboard
     - non-critical
   * - Credentials

       + the AWS account ``training-aws``, for the instructor
       + the MMS account ``advanced-ops+instructor@mongodb.com``, for the instructor
       + the MMS account ``advanced-ops+student@mongodb.com``, for the students
     - CRITICAL

If any of these requirements fail, please consult training@mongodb.com
and ce@mongodb.com for further information about whether you can deliver the session.

Prizes
~~~~~~

As an incentive for teams to get competitive, there should ideally be a prize for the
winning team. Please make sure you know how many people are going to be
attending the session and ensure you know how many people will be in each team.
Each member of the winning team should receive a prize. Prizes should be small
– some ideas of prizes include T-shirts, O’Reilly books, boxes of chocolates,
bottles of wine, small trophies.

Team Setup
~~~~~~~~~~

Firstly make sure you explain the plan for the next 2 days:

* Competitors will be divided into teams
* Teams will compete against each other in a series of tasks
* Tasks will revolve around real-life MongoDB scenarios
* Teams will need to identify the problem, propose and execute a solution
* Teams will be awarded points for speed, elegance and accuracy of the solution
* The team with the most points at the end of the second day will be declared
  winner of the training and will receive a prize

Make sure that the most experienced MongoDB competitors in the room (there are
usually 1 or 2 more experienced than the others) are on different teams. It
also makes sense to mix in Developers with Operations so there are balanced
knowledge pools in each team. Give teams 2 minutes to relocate around a single
“team” machine in the classroom, and to come up with a team name.

After people have moved around to their team machines, assign each team a group
number and write them up on the whiteboard, scores will be written up against
them here.

Each team will have their own assigned EC2 instances. And for the most part,
should work entirely out of the ``/home/ec2-user/scripts`` directory and ``mongo``
shell on their dedicated virtual machines.

MMS Credentials
~~~~~~~~~~~~~~~

Some exercises require you and the students to use MMS.
You should log in to MMS as the user ``advanced-ops+instructor@mongodb.com``,
and students should log in as ``advanced-ops+student@mongodb.com``.

If you're missing the password to either of these accounts, contact ``training@mongodb.com``
to get access.

Installing and configuring the ``aws-cli`` tool
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install ``aws-cli``
+++++++++++++++++++

Check whether you have ``aws-cli`` installed by running::

    $ aws --version

If it isn't installed, you can install it using pip::

    $ sudo pip install awscli

If you don't have pip, you can download it here: https://pip.pypa.io/en/latest/installing.html

Get access to the ``training-aws`` account
++++++++++++++++++++++++++++++++++++++++++

The AWS admin for training needs to give you a username and password to use for
accessing the the ``training-aws`` account. Contact ``training@mongodb.com`` if
you haven't received these.

Sign in to the AWS console at
https://mongodb-training-aws.signin.aws.amazon.com/console. You will be required
to change your password the first time you log in.

Generate an AWS API key
+++++++++++++++++++++++

From the AWS console home (the view that lists all AWS services), under
"Administration and Security", click "Identity & Access Management", then click
"Users" on the left sidebar. In the list of usernames, click your username, then
scroll down and click "Manage Access Keys", then click "Create Access Key".
Click "Show User Security Credentials" and leave this window open so you can
copy and paste the keys in the next step.

Configure ``aws-cli`` to use your API key
+++++++++++++++++++++++++++++++++++++++++

Run ::

    $ aws configure --profile wargaming

and when prompted, fill in the following values::

    AWS Access Key ID [None]: [paste the Access Key ID here]
    AWS Secret Access Key [None]: [paste the Secret Access Key here]
    Default region name [None]: us-east-1
    Default output format [None]: text

There should now be a file named ``~/.aws/config`` containing the following::

    [profile wargaming]
    aws_access_key_id = [your Access Key ID]
    aws_secret_access_key = [your Secret Access Key]
    region = us-east-1
    output = text

You can close the window from the previous step, and ignore the warning ("You
haven't downloaded the User security credentials. This is the last time these
credentials will be available for download."). If you ever lose your AWS API key
you can generate a new one.

Verify that you can authenticate
++++++++++++++++++++++++++++++++

Run ::

    $ aws ec2 describe-regions --profile wargaming

Verify that you can spin up instances
+++++++++++++++++++++++++++++++++++++

Open the EC2 console in a browser, then open a shell and cd to the
``admin-administrators-training/instance-launch`` directory and run ::

    $ ./repl.sh 1 [Your Name]
    $ ./shutDownRepl.sh

You should see one instance called "TrainingReplTeam-1-Your-Name" be created then terminated.

Launching Instances
~~~~~~~~~~~~~~~~~~~

1. To launch the initial instances for the groups for all sections other than
   `Performance` go into the Advanced Administrators' Training repo located at
   ``training/advanced-administrators-training/`` and go into the
   `instance-launch` directory. To run any of the scripts in this directory you
   must have the Amazon ``aws-cli`` tool installed and configured on your machine. If
   you don't have the Amazon ``aws-cli`` tool installed on your machine, see the following
   section for installation instructions.

   To launch a node for each team with the preloaded scripts and data sets run
   the following command ``advanced-administrators-training/instance-launch/repl.sh
   [Number of teams] [Your Name]`` We use your name so that the instances can be
   associated with you.

   The script should return to you an instance ID. Give it a minute or two for
   all of the instance to launch and become available. To give the teams the IP
   addresses to connect to, run the ``advanced-administrators-training/instance-launch/getReplIPs.sh``
   script and the output should give you what you need to get started.


2. To launch the sharded cluster for the performance and sharding exercise,
   you'll want to run ``advanced-administrators-training/instance-launch/shard.sh
   [Number of teams] [Your Name]``.  It should be noted that by default *this script
   will launch 8 machines per team* - 2 shards with 3 member replica
   sets each, a mongos, and a config server. This can add up if you have a lot
   of teams - be mindful of EC2 account limits!

   The script should take about 10 minutes (in total, not per-team). You might
   want to leave the AWS console open so you can keep an eye on its progress.
   When it's done it will print the public DNS names of the instances, along
   with which team each instance belongs to. You can also run
   ``advanced-administrators-training/instance-launch/getShardIPs.sh`` to print them
   out again.

Note: if you ran this training before 2015, you may have needed to run this
script hours in advance because it took so long. This should not be necessary
any more; it usually takes about 10 minutes.

Scoring
~~~~~~~

Teams are awarded up to 5 points per exercise based on the following criteria:

•	Speed of solution
•	Elegance of solution
•	Effectiveness of solution

Even if teams do not fully complete the exercise in practice, they can still be
awarded points for coming up with a theoretical solution.

Use the following table as a rough guide for awarding points:

.. list-table::
   :header-rows: 1
   :widths: 80, 20

   * - **Outcome**
     - **Points**
   * - Exercise completed within the time frame, and correct result achieved with
       most effective method.
     - 5
   * - Exercise completed within the time frame, correct result achieved, but most
       effective method not used.
     - 4
   * - Exercise not completed on time, but there is a sound theoretical
       strategy and if there had been more time they would have completed the task.
     - 3
   * - Exercise not completed, no real strategy but some good technical ideas
       tried.
     - 2
   * - Exercise not completed, no strategy and/or went down the wrong path.
     - 1

*N.B. From experience, most teams will not complete the exercises in the time
frame. Use your best judgment as to which team is the stronger one on each
exercise and award points accordingly.*

Exercises
~~~~~~~~~

There are a range of different exercise topics to get through during the day.
The idea is to cover all key areas of MongoDB – Backup and Restore, Sharding,
Replica Set Maintenance, Schema/Aggregation and Security practices.

It is important to get an understanding of the architecture of the customer
before you arrive. It may make no sense to spend time working on a sharding
exercise if the customer never intends to shard (although it might possibly be
useful in future in case they do). Present each team with the scenario, which
can also be read by them in their attendee PDF.

Some exercises will take longer than others. For example, the backup and
sharded performance exercises are probably half a day each, whereas the rolling
replica set upgrades are only 30 minutes or so. Depending how experienced the
teams are with the aggregation framework, the time frame can range up to a
couple of hours to deliver an aggregation statement. After the time for each
exercise has expired, go around each team and ask them to provide the step by
step for their solution, and find out whether they completed the task or not.
Award points based on the criteria above. Then spend a short amount of time
going through the correct solution, detailed in this guide.

After each exercise, allow a 5 minute break to set up the following task.


Virtual Machines
~~~~~~~~~~~~~~~~

Outside Internet access for the competitors is vital so they can access the
virtual machines running in Amazon EC2.

The VMs are ``M1.small`` instances running Amazon Linux. SSH'ing to
the instances will require the *PEM file* contained in the Advanced Administrators'
Training Git repository. You will need to ensure that the PEM file has been
distributed to the competitors in order for them to connect to the instances.
You will also need the IP addresses listed from the ``/<path-to-wargaming-repo>/
instance-launch/getReplIPs.sh`` script. Give each time their virtual
machine IP addresses.

From the terminal on a Linux/Mac machine, connect with the following command::

  ssh ec2-xx-xxx-xx-xx.compute-1.amazonaws.com \
      -l ec2-user –i /path/to/AdvancedOpsTraining.pem

When connecting from a Windows machine, ensure there is a suitable SSH client
installed that can handle file authentication, such as PuTTY and PuTTYgen. See
the following article for information on using PEM files with PuTTY:

http://support.cdh.ucla.edu/help/132-file-transfer-protocol-ftp/583-converting-your-private-key-

Users should log in as ``ec2-user``, which has ``sudo`` access.
Each team will have their own instance to connect to in order to complete each exercise.

Backups and Recovery
~~~~~~~~~~~~~~~~~~~~

.. include:: sections/instructor-backups.rst


Replication
~~~~~~~~~~~

.. include:: sections/instructor-replication.rst


Aggregation Framework + Map-Reduce
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. include:: sections/instructor-agg.rst


Sharding & Performance Troubleshooting
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. include:: sections/instructor-perf.rst

Security
~~~~~~~~

.. include:: sections/instructor-security.rst


Shutting Down & Rebuilding Clusters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To shutdown the nodes launched for each team run `shutDownRepl.sh`: this will
terminate all the teams' instances but not the sharded clusters.

To shutdown the sharded clusters run `shutDownCluster.sh`: this will terminate
the shards, config server, and mongos.

These will only remove the nodes launched by the previous execution of
`repl.sh` and `shard.sh`. If you ran either of the launch commands twice in a
row to rebuild a cluster, you will have to log on to the EC2 dashboard,
filter on "Advanced Administrators' Training" and terminate the instances there. At
the end of an Advanced Administrators' Training session, *ALWAYS* log on to the
EC2 dashboard to make sure all of the instances launched by you have been
terminated.
