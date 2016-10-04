#!/bin/bash

# Show all active stacks in all used regions

SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROFILES=`cat $SCRIPTDIR/profiles.txt`

for profile in ${PROFILES[@]}; do
  echo Region: $profile
  $SCRIPTDIR/../describe.py --profile ${profile}
  echo ""
done