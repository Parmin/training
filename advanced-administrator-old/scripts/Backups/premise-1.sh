#!/bin/bash

export MONGOPATH=/home/ec2-user/new/bin
export PATH="$PATH:$MONGOPATH"
mms_install_agent_docs='https://docs.mms.mongodb.com/tutorial/install-automation-agent-with-rpm-package/'


echo 'Checking for MMS automation agent...'
if ! rpm -qi mongodb-mms-automation-agent-manager.x86_64 > /dev/null
then
    # agent not installed
    echo
    echo 'The MMS automation agent is not installed'
    echo "Follow the instructions here: $mms_install_agent_docs"
    exit 1
fi
if ! service mongodb-mms-automation-agent status > /dev/null
then
    # agent not running
    echo
    echo 'The MMS automation agent is not running'
    echo "Finish following the instructions here: $mms_install_agent_docs"
    exit 1
fi


check_replset() {
    # Check that some mongod is running on port 27017, 27018, 27019
    echo 'Checking for a replica set...'
    for port in 27017 27018 27019
    do
        if ! $MONGOPATH/mongo --quiet --eval ';' --port $port
        then
            echo "  No mongod running on port $port"
            return 1
        fi
    done
}
if ! check_replset
then
    echo "Starting a replica set on 27017, 27018, 27019"
    sudo killall mongod
    # Wait for mongods to die
    while { sleep 0.5; pids="$(ps -Cmongod >/dev/null)"; }
    do
        echo "Waiting for mongod (pids $pids) to shut down..."
    done
    sudo rm -rf /data/node{1,2,3}
    sudo sudo -u mongod mkdir /data/node{1,2,3}

    export MONGOPATH=/home/ec2-user/new/bin
    export PATH=$PATH:$MONGOPATH
    # set up the replica set nodes
    for i in 1 2 3
    do
        sudo sudo -u mongod $MONGOPATH/mongod \
            --dbpath /data/node$i \
            --replSet rs-"$(hostname)" \
            --port $(( 27017 + (i - 1) )) \
            --fork \
            --logpath /tmp/mongo$i.log \
            --nojournal \
            --smallfiles || exit $?
    done
    sleep 30
    $MONGOPATH/mongo --eval '
    printjson(rs.initiate({
        "_id": "rs-'"$(hostname)"'",
        "members" : [
            { "_id" : 0, "host" : "localhost:27017" },
            { "_id" : 1, "host" : "localhost:27018" },
            { "_id" : 2, "host" : "localhost:27019" }
        ]}))
    '
    echo
    echo 'Done setting up a replica set.'
    echo 'Go to the MMS console and import this instance for Monitoring,'
    echo 'install the Monitoring Agent, and enable Backup.'
    exit 1
fi


echo 'Checking for MMS backups...'
# Check that they have started backups
if ! $MONGOPATH/mongo --quiet local \
    --eval '
    var n = db.oplog.rs.find({ "o.backup_token": {$exists: 1}}).count();
    if (n == 0) {
       quit(1);
    }
    '
then
    # no backup token found in oplog
    echo
    echo 'Go to the MMS console and import this instance for Monitoring,'
    echo 'install the Monitoring Agent, and enable Backup.'
    exit 1
fi


echo 'Executing the scenario...'
# TODO also run operations on other collections, to make the scenario more
# interesting / realistic
$MONGOPATH/mongo --quiet --eval '
load("scripts/data.js");
assert.eq(0, db.users.count());

var n = 20000;
insertUserData(db.users, n);
assert.eq(n, db.users.count());

db.users.drop();
assert.eq(0, db.users.count());
'


echo 'Done'
