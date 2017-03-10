Premise 1
+++++++++

.. start-premise-one

"*Whoops! The new intern was in charge of writing a reporting job that
would run nightly on your systems during off-peak hours (it takes hours to
complete!) and he thought it would be a good idea to test if it works
in production in the middle of your business day! Now your CPU is
spiking and your prod system is sluggish.  Deal with it.*"

.. end-premise-one

Instances
+++++++++

For this section, teams will use different EC2 machines. The
instructor will prove the IP address for a ``mongos`` instance
connected to a sharded cluster.

Premise 2
+++++++++

.. start-premise-two

"*You have noticed drastic performance issues with your MongoDB
deployment.  Queries are slow, responsiveness is generally slow, and
updates take quite some time as well.*

*You have tried a number of things to boost performance. You started
reading off secondaries, reworked some of your queries, and even
expanded to a sharded cluster.*

*So far nothing has worked and performance has stayed exactly the
same. This is it, your last ditch effort to fix EVERYTHING that is
wrong with this deployment. And if you can't fix it, or it will take a
long time, identify what the problem is and come up with a plan of
action to fix it.*"

The long-running queries include:

- finding users by screen name::

    db.live.find( { "user.screen_name" : "____thaaly" } )

- finding all users who have a particular name e.g. Beatriz::

    db.live.find( { "user.name" : /Beatriz/ } )

- finding all users in the Brasilia timezone with more than 70 friends, and sorting by most friends::

    db.live.find( { "user.time_zone" : "Brasilia",
                    "user.friends_count" : { $gt : 70 } } )
             .sort( { "user.friends_count" : -1 } )

Please investigate all possible causes of slow queries and slow system
responsiveness.

.. end-premise-two

.. include:: newpage.tmpl
