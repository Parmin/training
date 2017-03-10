#!/bin/bash

# kill all existing mongod's
killall -9 mongod

# delete any existing directories
rm -rf /data/node1
rm -rf /data/node2
rm -rf /data/node3

# set up new data directories
mkdir /data/node1
mkdir /data/node2
mkdir /data/node3

export MONGOPATH=/home/ec2-user/new/bin

# set up the replica set nodes
$MONGOPATH/mongod --dbpath /data/node1 --replSet rs0 --port 27017 --fork --logpath /tmp/mongo1.log --nojournal --smallfiles
wait $!
$MONGOPATH/mongod --dbpath /data/node2 --replSet rs0 --port 27018 --fork --logpath /tmp/mongo2.log --nojournal --smallfiles
wait $!
$MONGOPATH/mongod --dbpath /data/node3 --replSet rs0 --port 27019 --fork --logpath /tmp/mongo3.log --nojournal --smallfiles
wait $!

sleep 30

$MONGOPATH/mongo --eval "rs.initiate({ '_id': 'rs0', 'members' : [{ '_id' : 0, 'host' : 'localhost:27017' },{ '_id' : 1, 'host' : 'localhost:27018' },{ '_id' : 2, 'host' : 'localhost:27019' } ]})"


