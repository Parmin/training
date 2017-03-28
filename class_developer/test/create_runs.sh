#!/bin/bash

# Create a test run in all regions, then wait for them to be completed

SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ADVADMINDIR="$SCRIPTDIR/../../advanced_administrator"

PROFILES=`cat $SCRIPTDIR/profiles.txt`
KEYPAIR=AdvancedAdministrator

for profile in ${PROFILES[@]}; do
  echo Creating Run for Region: $profile
  # TODO - make the string unique
  RUN=systest-${USER}
  ${ADVADMINDIR}/deploy.py --profile ${profile} --run ${RUN} --teams 1 --testmode --noom
  echo ""
done

# Iterate on all regions, waiting for the run to be completed or rolledback
for profile in ${PROFILES[@]}; do
  echo Waiting on Run creation for Region: $profile
  DONE=false
  while [ $DONE == false ]; do
    OUT=`${ADVADMINDIR}/describe.py --profile ${profile} | grep CREATE_IN_PROGRESS`
    if [ -z "$OUT" ]; then
      DONE=true
      ${ADVADMINDIR}/describe.py --profile ${profile}
      echo ""
    else
      sleep 30
    fi
  done
done
