#!/usr/bin/env bash
echo 'db.testCollection.drop();  //clean up the collection.' | mongo --port 27017 readConcernTest; wait
echo 'db.testCollection.insertOne( { message : "This document is probably on at least one secondary." } );' | mongo --port 27017 readConcernTest; wait
echo 'db.fsyncLock()' | mongo --port 27018; wait
echo 'db.fsyncLock()' | mongo --port 27019; wait
echo 'db.testCollection.insertOne( { message : "This document is only on the primary." } );' | mongo --port 27017 readConcernTest; wait
echo 'db.testCollection.find().readConcern("majority");' | mongo --port 27017 readConcernTest; wait
echo 'db.testCollection.find();  // read concern "local"' | mongo --port 27017 readConcernTest; wait
echo 'db.fsyncUnlock()' | mongo --port 27018; wait
echo 'db.fsyncUnlock()' | mongo --port 27019; wait
echo 'db.testCollection.drop();  //clean up the collection.' | mongo --port 27017 readConcernTest










