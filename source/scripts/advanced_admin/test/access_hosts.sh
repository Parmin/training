#!/bin/bash

# Create a test run in all regions, then using the AdvancedAdministrator key/pair, access all hosts

PROFILES=`cat profiles.txt`
KEYPAIR=AdvancedAdministrator

cd ..

for profile in ${PROFILES[@]}; do
  echo Region: $profile
  # TODO - make the string unique
  RUN=systest-${USER}
  ./manage.py   --profile ${profile} --run ${RUN} --roles all --teams all --cmd "/bin/hostname -f"
  echo ""
done