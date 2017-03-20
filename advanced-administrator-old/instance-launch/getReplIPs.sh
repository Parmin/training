#!/bin/bash

for i in `cat repl_instances`; do
	result=$(aws ec2 --profile wargaming describe-instances --instance-ids $i --output json)
    echo "$result" | python -c '
import sys,json
v = json.load(sys.stdin)["Reservations"][0]["Instances"][0]
print filter(lambda t: t["Key"] == "Name", v["Tags"])[0]["Value"], v["PublicIpAddress"]
    '
done
