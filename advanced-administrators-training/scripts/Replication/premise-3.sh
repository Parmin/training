#!/bin/bash

export MONGOPATH=/home/ec2-user/new/bin

sudo killall mongod

sudo rm -rf /data/rs1 /data/rs2 /data/rs3 /tmp/replset

sudo sudo -u mongod mkdir -p /data/rs1 /data/rs2 /data/rs3 /tmp/replset

sudo sudo -u mongod $MONGOPATH/mongod --replSet rs0 --logpath /tmp/replset/1.log --dbpath /data/rs1 --port 27017 --oplogSize 2 --fork --nojournal --smallfiles
sudo sudo -u mongod $MONGOPATH/mongod --replSet rs0 --logpath /tmp/replset/2.log --dbpath /data/rs2 --port 27018 --oplogSize 2 --fork --nojournal --smallfiles
sudo sudo -u mongod $MONGOPATH/mongod --replSet rs0 --logpath /tmp/replset/3.log --dbpath /data/rs3 --port 27019 --oplogSize 2 --fork --nojournal --smallfiles

sleep 3

sleep 30
$MONGOPATH/mongo --eval "rs.initiate({ '_id': 'rs0', 'members' : [{ '_id' : 0, 'host' : 'localhost:27017' },{ '_id' : 1, 'host' : 'localhost:27018' },{ '_id' : 2, 'host' : 'localhost:27019' } ]})"
sleep 45

$MONGOPATH/mongo --eval "for (i = 0; i < 1000; i++ ) db.col.insert( { val : 'a' })"

sleep 10

$MONGOPATH/mongo --port 27019 --eval "db.adminCommand( { shutdown : 1 })"

sleep 10

$MONGOPATH/mongo --eval "for (i = 0; i < 200000; i++ ) db.col.insert( { val : 'a' })"

sudo sudo -u mongod $MONGOPATH/mongod --replSet rs0 --logpath /tmp/replset/3.log --dbpath /data/rs3 --port 27019 --oplogSize 2 --fork --nojournal --smallfiles


