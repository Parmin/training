#!/bin/bash

# kill all existing mongod's
sudo killall -9 mongod

# delete any existing directories
sudo rm -rf /data/node1
sudo rm -rf /data/node2
sudo rm -rf /data/node3

# set up new data directories, as user mongod to support importing into MMS Automation
sudo sudo -u mongod mkdir /data/node1
sudo sudo -u mongod mkdir /data/node2
sudo sudo -u mongod mkdir /data/node3

export MONGOPATH=/home/ec2-user/old/bin

# set up the replica set nodes
sudo sudo -u mongod $MONGOPATH/mongod --dbpath /data/node1 --replSet rs0 --port 27017 --fork --logpath /tmp/mongo1.log --nojournal --smallfiles
sudo sudo -u mongod $MONGOPATH/mongod --dbpath /data/node2 --replSet rs0 --port 27018 --fork --logpath /tmp/mongo2.log --nojournal --smallfiles
sudo sudo -u mongod $MONGOPATH/mongod --dbpath /data/node3 --replSet rs0 --port 27019 --fork --logpath /tmp/mongo3.log --nojournal --smallfiles

sleep 30
$MONGOPATH/mongo --eval "rs.initiate({ '_id': 'rs0', 'members' : [{ '_id' : 0, 'host' : 'localhost:27017' },{ '_id' : 1, 'host' : 'localhost:27018' },{ '_id' : 2, 'host' : 'localhost:27019' } ]})"
sleep 30

$MONGOPATH/mongo --quiet --eval '
load("scripts/data.js");
assert.eq(0, db.users.count());

var n = 20000;
insertUserData(db.users, n);
assert.eq(n, db.users.count());
'

echo 'Done'
