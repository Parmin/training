#!/bin/bash -e

aws ec2 --profile wargaming terminate-instances --instance-ids `cat sharded_instances`
rm sharded_instances
