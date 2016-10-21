#!/bin/bash

# Create a test run in all regions, then using the AdvancedAdministrator key/pair, access all hosts

SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ADVADMINDIR="$SCRIPTDIR/../../advanced_admin"

PROFILES=`cat $SCRIPTDIR/profiles.txt`
KEYPAIR=AdvancedAdministrator

for profile in ${PROFILES[@]}; do
  echo Region: $profile
  # TODO - make the string unique
  RUN=systest-${USER}
  ${ADVADMINDIR}/manage.py --profile ${profile} --run ${RUN} --roles all --teams all --cmd "/bin/hostname -f"
  echo ""
done