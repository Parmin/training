#!/bin/bash

for id in $(cat repl_instances)
do
    aws ec2 --profile wargaming terminate-instances --instance-ids "$id"
done
rm repl_instances
