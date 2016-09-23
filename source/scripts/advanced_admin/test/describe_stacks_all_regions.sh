#!/bin/bash

# Show all active stacks in all used regions

PROFILES=`cat profiles.txt`

for profile in ${PROFILES[@]}; do
  echo Region: $profile
  ../describe.py --profile ${profile}
  echo ""
done