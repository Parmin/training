#!/bin/bash

max_teams=5

if [[ ! $# == 2 ]]
then
	echo "Usage: [number of teams] [Requester]"
	exit 1
fi
count="$1"
requester="$2"


if [[ "$count" -gt "$max_teams" ]]
then
    echo "Only up to $max_teams teams are currently supported"
    exit 1
fi

echo "launching $count security (ldap/ssl) instances for $requester"

ami_id=ami-825b66ea

echo 'launching' $ami_id


for i in $(seq $count)
do
    team_number=$i
    team_name=team0$team_number

    echo "Starting the ${i}th instance as team $team_name"
    result=$(aws ec2 --profile wargaming run-instances \
        --image-id $ami_id \
        --key-name AdvancedOpsTraining \
        --security-groups default \
        --count 1 \
        --instance-initiated-shutdown-behavior 'terminate' \
        --output json \
        --instance-type 'm3.medium')

    instance_id="$(echo "$result" | python -c 'import sys,json;print json.load(sys.stdin)["Instances"][0]["InstanceId"]')"
	echo "  got id $instance_id"
    echo "$instance_id" >> repl_instances

	name="TrainingSecurityTeam-$team_number-$requester"

    # TODO(dpercy): it looks like there is a race condition where the instances
    # may not have started when we try to tag them:
	# 
	# A client error (InvalidInstanceID.NotFound) occurred when calling the CreateTags operation:
	# The instance ID 'i-922e5468' does not exist
    #
    # But I'm not sure if it's possible to avoid this.
	aws ec2 --profile wargaming create-tags \
        --tags "Key=Name,Value=$name" "Key=requestor,Value=$2" \
        --resources "$instance_id"
done
