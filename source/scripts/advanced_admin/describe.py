#! /usr/bin/env python

# Issues:

# TODO
#   - have a test mode where we can recover the info from a set of files, instead of a live cluster in order to run unit tests
#   - if a machine is restarted it would have a different external name and IP
#   - test if the run is completely created before reporting on it
#   - search for added teams after the initial top stack was created (tags?)

'''
Example of a run:
  ./describe --profile training-eu-west --run dcoupal-test --out /tmp/cluster.out

Example of an output:

Name: dcoupal-test1
KeyPair: AdvancedAdministrator
NumberOfTeams: 3

Teams:

  Id: 1
  LoadBalancer: dcoupal-t-OpsMgrLB-19CM34ELUH5OH-628727658.us-west-1.elb.amazonaws.com
  SecurityGroup: sg-3c0f3d58
  VPC: vpc-a0998bc5
  SubnetMask: 10.0.0.0/24
  Hosts:
    Id: i-27945293  Role: node1
    PrivateIP: 10.0.0.101       PrivateName: ip-10-0-0-101.us-west-1.compute.internal
    PublicIP: 54.183.69.202    PublicName: ec2-54-183-69-202.us-west-1.compute.amazonaws.com

...

    Id: i-25945291  Role: opsmgr1
    PrivateIP: 10.0.0.21        PrivateName: ip-10-0-0-21.us-west-1.compute.internal
    PublicIP: 54.153.109.82    PublicName: ec2-54-153-109-82.us-west-1.compute.amazonaws.com

    Id: i-b3925407  Role: opsmgr2
    PrivateIP: 10.0.0.22        PrivateName: ip-10-0-0-22.us-west-1.compute.internal
    PublicIP: 54.183.42.201    PublicName: ec2-54-183-42-201.us-west-1.compute.amazonaws.com

    Id: i-f0955344  Role: opsmgr3
    PrivateIP: 10.0.0.23        PrivateName: ip-10-0-0-23.us-west-1.compute.internal
    PublicIP: 54.153.122.132   PublicName: ec2-54-153-122-132.us-west-1.compute.amazonaws.com


  Id: 2
  LoadBalancer: dcoupal-t-OpsMgrLB-COTFCKJD1ZP9-1737778154.us-west-1.elb.amazonaws.com
  SecurityGroup: sg-3d0f3d59
  VPC: vpc-a1998bc4
  SubnetMask: 10.0.0.0/24
  Hosts:
    Id: i-f1955345  Role: node1
    PrivateIP: 10.0.0.101       PrivateName: ip-10-0-0-101.us-west-1.compute.internal
    PublicIP: 54.183.40.84     PublicName: ec2-54-183-40-84.us-west-1.compute.amazonaws.com
...
'''

import logging
import argparse
import sys
from datetime import date,timedelta
import time
from provisioner_aws_cf import Provisioner_aws_cf
from provisioner_aws_plain import Provisioner_aws_plain

from provider_utils import *

FORMAT = '%(asctime)-15s %(message)s'

def setup_logging(logger):
    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setLevel(logging.DEBUG)
    consoleHandler.setFormatter(logging.Formatter(FORMAT))

    logger.addHandler(consoleHandler)

def main():
    logger = logging.getLogger(__name__)
    setup_logging(logger)

    parser = argparse.ArgumentParser(description='Describe the resources used by a training class')
    parser.add_argument('--run', dest='training_run', type=str,
      help="environment training run identifier, or none to see all the runs")

    parser.add_argument('--out', dest='out', type=str,
      help="File(s) in which to store the output. For each team, a -X is added to the name")

    parser.add_argument('--profile', dest='awsprofile', default='default', type=str,
      help="AWS profile that will launch the environment")

    parser.add_argument('--provider', dest='provider', default="aws-cf", type=str,
      help="Provider, one of 'aws-cf' or 'aws-plain'")

    parser.add_argument('--verbose', dest='verbose', action='store_true',
      help="Show more details in the output")

    args = parser.parse_args()
    logger.info("Collected the following arguments {0}".format(args))

    training_run = args.training_run
    awsprofile = args.awsprofile

    provisioner_values = ["aws-plain", "aws-cf"]

    if args.provider == "aws-cf":
        pr = Provisioner_aws_cf(args, training_run, aws_profile=awsprofile)
    elif args.provider == "aws-plain":
        logger.setLevel(logging.DEBUG)
        pr = Provisioner_aws_plain(training_run, aws_profile=awsprofile)
    else:
        fatal(1, "Invalid provider, must be one of {}".format(provisioner_values))

    pr.connect()
    build_id = date.today().strftime("%Y-%m-%d:%H:%M:%S")
    logger.debug("Describing run: {0}".format(training_run))
    pr.describe()


if __name__ == "__main__":
    main()
