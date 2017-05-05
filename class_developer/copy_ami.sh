#!/bin/bash

# Script to copy an AMI to the list of regions we support

AMI="$1"

REGIONS=`cat test/regions.txt`
MAIN_REGION=us-east-1
MAIN_REGION_PROFILE=training-us-east-1
KEYPAIR=AdvancedAdministrator

if [ -z "$AMI" ]; then
  echo You must provide an AMI Id as the source to copy
  exit 1
fi

AMI_NAME=`aws --profile ${MAIN_REGION_PROFILE} ec2 describe-images --image-ids ${AMI} | jq -r '.Images[0].Name'`
if [ -z "$AMI_NAME" ]; then
  exit 1
fi

echo Copying AMI ${AMI}/${AMI_NAME} from ${MAIN_REGION} to other regions
for region in ${REGIONS[@]}; do
  echo Region: $region
  if [ ${MAIN_REGION} == ${region} ]; then
    echo Skipping copying into self...
  else
    DESCRIPTION="Copy of ${AMI_NAME}/${AMI} in region ${MAIN_REGION}"
    CMD="aws ec2 copy-image --source-image-id ${AMI} --source-region ${MAIN_REGION} --region ${region} --name \"${AMI_NAME}\" --desc \"${DESCRIPTION}\""
    echo $CMD
    eval $CMD
  fi
  echo ""
done
