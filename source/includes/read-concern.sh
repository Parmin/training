# BEGIN SCRIPT
#!/usr/bin/env bash
echo 'db.testCollection.drop();' | mongo --port 27017 readConcernTest; wait
echo 'db.testCollection.insertOne({message: "probably on a secondary." } );' |
     mongo --port 27017 readConcernTest; wait
echo 'db.fsyncLock()' | mongo --port 27018; wait
echo 'db.fsyncLock()' | mongo --port 27019; wait
echo 'db.testCollection.insertOne( { message : "Only on primary." } );' |
     mongo --port 27017 readConcernTest; wait
echo 'db.testCollection.find().readConcern("majority");' |
     mongo --port 27017 readConcernTest; wait
echo 'db.testCollection.find(); // read concern "local"' |
     mongo --port 27017 readConcernTest; wait
echo 'db.fsyncUnlock()' | mongo --port 27018; wait
echo 'db.fsyncUnlock()' | mongo --port 27019; wait
echo 'db.testCollection.drop();' | mongo --port 27017 readConcernTest
# END SCRIPT
