#!/bin/bash
set -e

cd "$(dirname "$0")"

aws ec2 --profile wargaming describe-instances \
 --instance-id $(cat sharded_instances) \
 --output json | python -c '
import sys, json
for r in json.load(sys.stdin)["Reservations"]:
    for i in r["Instances"]:
        requestor = [t["Value"] for t in i["Tags"] if t["Key"] == "Name"]
        print requestor[0] if requestor else "(no-requestor-specified)", i["PublicDnsName"]
' | sort
