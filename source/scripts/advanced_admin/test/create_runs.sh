#!/bin/bash

# Create a test run in all regions, then wait for them to be completed

PROFILES=`cat profiles.txt`
KEYPAIR=AdvancedAdministrator

cd ..

for profile in ${PROFILES[@]}; do
  echo Creating Run for Region: $profile
  # TODO - make the string unique
  RUN=systest-${USER}
  ./deploy.py --profile ${profile} --run ${RUN} --keypair ${KEYPAIR} --teams 1 --testmode
  echo ""
done

# Iterate on all regions, waiting for the run to be completed or rolledback
for profile in ${PROFILES[@]}; do
  echo Waiting on Run creation for Region: $profile
  DONE=false
  while [ $DONE == false ]; do
    OUT=`./describe.py --profile ${profile} | grep CREATE_IN_PROGRESS`
    if [ -z "$OUT" ]; then
      DONE=true
      ./describe.py --profile ${profile}
      echo ""
    else
      sleep 30
    fi
  done
done
