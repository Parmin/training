#!/bin/bash

# Destroy all test runs in all regions, then wait for them to be completed

SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ADVADMINDIR="$SCRIPTDIR/../../advanced_admin"

PROFILES=`cat $SCRIPTDIR/profiles.txt`
KEYPAIR=AdvancedAdministrator

for profile in ${PROFILES[@]}; do
  echo Destroying Run for Region: $profile
  # TODO - make the string unique
  RUN=systest-${USER}
  ${ADVADMINDIR}/teardown.py --profile ${profile} --run ${RUN}
  echo ""
done

# Iterate on all regions, waiting for the run to be completed or rolledback
for profile in ${PROFILES[@]}; do
  echo Waiting on Run deletion for Region: $profile
  DONE=false
  while [ $DONE == false ]; do
    OUT=`${ADVADMINDIR}/describe.py --profile ${profile} | grep DELETE_IN_PROGRESS`
    if [ -z "$OUT" ]; then
      DONE=true
      ${ADVADMINDIR}/describe.py --profile ${profile}
      echo ""
    else
      sleep 30
    fi
  done
done
