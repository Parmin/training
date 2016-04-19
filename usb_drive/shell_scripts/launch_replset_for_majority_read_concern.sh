#!/usr/bin/env bash

mkdir -p /data/replset/{1,2,3}
wait
mongod --replSet majrc --port 27017 --dbpath /data/replset/1 --logpath /data/replset/1/mongod.log --wiredTigerCacheSizeGB 1 --enableMajorityReadConcern --fork
wait
mongod --replSet majrc --port 27018 --dbpath /data/replset/2 --logpath /data/replset/2/mongod.log --wiredTigerCacheSizeGB 1 --enableMajorityReadConcern --fork
wait
mongod --replSet majrc --port 27019 --dbpath /data/replset/3 --logpath /data/replset/3/mongod.log --wiredTigerCacheSizeGB 1 --enableMajorityReadConcern --fork
wait
echo 'cfg = { "_id" : "majrc", "members" : [ { "_id" : 0, "host" : "localhost:27017", } ] }; rs.initiate(cfg)' | mongo
wait
echo 'rs.add("localhost:27018")' | mongo
wait
echo 'rs.add("localhost:27019")' | mongo
