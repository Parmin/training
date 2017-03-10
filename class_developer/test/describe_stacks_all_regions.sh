#!/bin/bash

# Show all active stacks in all used regions

SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ADVADMINDIR="$SCRIPTDIR/../../advanced_administrator"

PROFILES=`cat $SCRIPTDIR/profiles.txt`

for profile in ${PROFILES[@]}; do
  echo Region: $profile
  ${ADVADMINDIR}/describe.py --profile ${profile}
  echo ""
done
