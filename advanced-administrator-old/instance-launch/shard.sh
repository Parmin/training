#!/bin/bash
set -e

cd "$(dirname "$0")"

ami_id=ami-08c6b861  # old
ami_id=ami-00b2ff68  # Advanced Ops Sharded
ami_id=ami-3c9fd054  # Advanced Ops Sharded 2
ami_id=ami-b2ade4da  # Advanced Ops Sharded 3
ami_id=ami-3726145d  # Advanced Ops Sharded 4

SSH_KEY=../credentials/AdvancedOpsTraining.pem


function wait_for_ssh() {
    local hostname="$1"
    local ssh_err=.ssh_error
    echo >&2 -n "Waiting for instance boot and SSH..."
    output=""
    for i in {1..50}; do
        echo '  attempt' $i
        output="$(ssh_exec "$hostname" "echo 'hi'" 2>"$ssh_err" || true)"
        if [ "$output" = "hi" ]; then break; fi
        sleep 30
        #echo >&2 -n "."
    done
    echo >&2 ""

    echo end loop

    # Check if we have timed out
    if [ ! "$output" = "hi" ]; then
        echo >&2 "Failed to connect via SSH (timed out)"
        [ -f "$ssh_err" ] && cat "$ssh_err"
        exit 1
    fi
}

ssh_exec() {
    host="$1"
    shift
    ssh ec2-user@"$host" -i "$SSH_KEY" \
        -o "StrictHostKeyChecking no" \
        -o "UserKnownHostsFile /dev/null" \
        -o "BatchMode yes" \
        -o "ConnectTimeout 10" \
        "$@" || return $?
}

host_of_id() {
    aws ec2 --profile wargaming describe-instances --instance-id "$1" --output json |
        python -c 'import sys,json;print json.load(sys.stdin)["Reservations"][0]["Instances"][0]["PublicDnsName"]'
}


# outputs list of instance ids
start_instances() {
    local count="$1"

    local result=$(aws ec2 --profile wargaming run-instances \
        --image-id "$ami_id" \
        --key-name AdvancedOpsTraining \
        --security-groups default \
        --count "$count" \
        --output json \
        --instance-initiated-shutdown-behavior 'terminate')

    local instance_ids="$(echo "$result" | python -c 'import sys,json;print "\n".join(i["InstanceId"] for i in json.load(sys.stdin)["Instances"])')"

    echo "$instance_ids" >> sharded_instances  # so we can print IP addresses later
    echo "$instance_ids"
}

configure_replset() {
    local rsName="$1"
    # next 3 arguments are the instance ids
    local hostnames=(
        $(host_of_id "$2")
        $(host_of_id "$3")
        $(host_of_id "$4")
    )

    # start mongod on each instance
    for hostname in "${hostnames[@]}"
    do
        wait_for_ssh $hostname
        ssh_exec $hostname bash <<EOF
            mongodb/bin/mongod \
                --dbpath /data/db \
                --fork \
                --logpath /data/db/mongo.log \
                --nojournal \
                --smallfiles \
                --replSet $rsName
EOF
    done

    # configure the replica set
    ssh_exec ${hostnames[0]} bash <<EOF
        set -xv
        mongodb/bin/mongo --eval '
            printjson(rs.initiate());
            while (true) {
                var rss = rs.status();
                if (rss.members && rss.members[0].stateStr === "PRIMARY") {
                    break;
                }
                print("waiting for rs.initiate() to finish");
                sleep(1000);
            }
            printjson(rs.add("${hostnames[1]}"));
            printjson(rs.add("${hostnames[2]}"));
            printjson(rs.conf());
        '
EOF

    # move the datafiles for the twitter db into the dbpath
    for hostname in "${hostnames[@]}"
    do
        ssh_exec $hostname bash <<EOF
            shopt -s nullglob
            find /data/$rsName/ -name 'twitter*' -exec mv {} /data/db/ ';'

            # remove all the unused data
            rm -rf /data/rs0 /data/rs1 /data/config /data/mongos
EOF
    done
}


configure_config_server() {
    local hostname="$(host_of_id "$1")"

    wait_for_ssh $hostname
    ssh_exec $hostname bash <<EOF
        killall mongod

        # remove the data not used by a config server
        rm -rf /data/rs0 /data/rs1 /data/mongos /data/db

        # start mongod in standalone mode so we can hack the config database
        mongodb/bin/mongod --smallfiles --nojournal --dbpath /data/config --fork --logpath /dev/stderr

        # set the hostnames of the shards
        mongodb/bin/mongo config --eval '
            db.shards.update({ _id: "shard0000" }, {
                host: "rs0/$(host_of_id ${ids_rs0[0]}),$(host_of_id ${ids_rs0[1]}),$(host_of_id ${ids_rs0[2]})"
            });
            db.shards.update({ _id: "shard0001" }, {
                host: "rs1/$(host_of_id ${ids_rs1[0]}),$(host_of_id ${ids_rs1[1]}),$(host_of_id ${ids_rs1[2]})"
            });
        '

        # do a clean shutdown
        mongodb/bin/mongo admin --eval 'db.shutdownServer()'
        while ps -Cmongod >/dev/null
        do
            echo waiting for mongod to shut down...
            sleep 1
        done

        # restart as a config server
        mongodb/bin/mongod --smallfiles --nojournal --dbpath /data/config --configsvr --fork --logpath /data/config/mongod.log
EOF
}



configure_mongos() {
    local hostname="$(host_of_id "$1")"
    local confighost="$(host_of_id $id_config)"

    wait_for_ssh $hostname
    ssh_exec $hostname bash <<EOF
        killall mongos
        mongodb/bin/mongos --fork --logpath /data/mongos/mongos.log --configdb "$confighost"

        rm -rf /data/rs0 /data/rs1 /data/config /data/db
EOF
}


name_instance() {
    local instance_id="$1"
    local name="$2"
    local requester="$3"

    aws ec2 --profile wargaming create-tags \
        --tags "Key=Name,Value=$name-$requester" "Key=requestor,Value=$requester" \
        --resources "$instance_id"
}


create_cluster() {
    local team_id="$1"
    local requester="$2"


    local ids_rs0=($(start_instances 3))
    local ids_rs1=($(start_instances 3))
    local id_config="$(start_instances 1)"
    local id_mongos="$(start_instances 1)"

    name_instance "${ids_rs0[0]}" "team-$team_id-rs0-A" "$requester"
    name_instance "${ids_rs0[1]}" "team-$team_id-rs0-B" "$requester"
    name_instance "${ids_rs0[2]}" "team-$team_id-rs0-C" "$requester"

    name_instance "${ids_rs1[0]}" "team-$team_id-rs1-A" "$requester"
    name_instance "${ids_rs1[1]}" "team-$team_id-rs1-B" "$requester"
    name_instance "${ids_rs1[2]}" "team-$team_id-rs1-C" "$requester"

    name_instance "${id_config}" "team-$team_id-config" "$requester"
    name_instance "${id_mongos}" "team-$team_id-mongos" "$requester"


    configure_replset rs0 ${ids_rs0[@]}
    configure_replset rs1 ${ids_rs1[@]}

    configure_config_server $id_config
    configure_mongos $id_mongos
}


main() {
    if [ $# != 2 ]
    then
        echo >&2 "Usage: $(basename "$0") [number of teams] [requester]"
        return 1
    fi
    local num_teams="$1"
    local requester="$2"

    for team_id in $(seq "$num_teams")
    do
        # do each create_cluster in parallel
        create_cluster "$team_id" "$requester" &
    done
    wait

    ./getShardIPs.sh
}

main "$@"
