#!/bin/bash

# Show all active stacks in all used regions

SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ADVADMINDIR="$SCRIPTDIR/../../advanced_administrator"

REGIONS=`cat $SCRIPTDIR/regions.txt`

for region in ${REGIONS[@]}; do
  echo Region: $region
  ${ADVADMINDIR}/describe.py --region ${region}
  echo ""
done
