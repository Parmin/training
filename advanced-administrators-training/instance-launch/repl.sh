#!/bin/bash

max_teams=10

if [[ $# == 2 ]]
then
    lowest_team_num="1"
    highest_team_num="$1"
    requester="$2"
elif [[ $# == 3 ]]
then
    lowest_team_num="$1"
    highest_team_num="$2"
    requester="$3"
else
    cat <<EOF
Usage:
    $0 [number of teams] [requestor]
    $0 [lowest team number] [highest team number] [requestor]
EOF
	exit 1
fi

if [[ "$highest_team_num" -lt "$lowest_team_num" ]]
then
    # swap them
    tmp=$highest_team_num
    highest_team_num=$lowest_team_num
    lowest_team_num=$tmp
fi


if [[ "$highest_team_num" -gt "$max_teams" ]]
then
    echo "Only up to $max_teams teams are currently supported"
    exit 1
fi

if [[ "$lowest_team_num" -lt 1 ]]
then
    echo "The lowest team num must be 1 or greater."
    exit 1
fi

echo "launching instances numbered $lowest_team_num through $highest_team_num for $requester"

ami_id=ami-43c9c92a # Advanced Ops Replica
ami_id=ami-766f2b1e # Advanced Ops MMS
ami_id=ami-1413547c # Advanced Ops MMS 2
ami_id=ami-5099c438 # Advanced Ops Replica 3
ami_id=ami-6a8cd102 # Advanced Ops MMS 3
ami_id=ami-345a035c # Advanced Ops MMS 4
ami_id=ami-703b1c18 # Advanced Ops MMS 5
ami_id=ami-94183ffc # Advanced Ops MMS 6
ami_id=ami-0ef7d066 # Advanced Ops MMS 7  # trying to fix cloud init
ami_id=ami-1237117a # Advanced Ops MMS 8  # fix team-select.sh permissions
ami_id=ami-9c3214f4 # Advanced Ops MMS 9  #
ami_id=ami-5435143c # Advanced Ops MMS 10
ami_id=ami-1080a178 # Advanced Ops MMS 11 # fix premise-3.sh
ami_id=ami-8488a9ec # Advanced Ops MMS 12 # remove premise-4.sh
ami_id=ami-8707b7ec # Advanced Ops MMS 13 # increase groups to 10
ami_id=ami-0d201267 # Advanced Ops MMS 14 # update glibc, fix typo


echo 'launching' $ami_id


for i in $(seq $lowest_team_num $highest_team_num)
do
    team_number=$i
    team_name=team$(printf '%02d' $team_number)

    echo "Starting an instance as team $team_name"
    result=$(aws ec2 --profile wargaming run-instances \
        --image-id $ami_id \
        --key-name AdvancedOpsTraining \
        --security-groups default \
        --count 1 \
        --instance-initiated-shutdown-behavior 'terminate' \
        --output json \
        --user-data "#!/bin/bash
/home/ec2-user/scripts/team-select.sh $team_name
")

    instance_id="$(echo "$result" | python -c 'import sys,json;print json.load(sys.stdin)["Instances"][0]["InstanceId"]')"
	echo "  got id $instance_id"
    echo "$instance_id" >> repl_instances

	name="TrainingReplTeam-$team_number-$requester"

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
