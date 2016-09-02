#! /usr/bin/env python

# Issues:

# TODO
#   - have a test mode where we can recover the info from a set of files, instead of a live cluster in order to run unit tests


'''
Example of a run:
  ./describe --profile training-eu-west --run dcoupal-test --out /tmp/cluster.out

Example of an output:

Name: dcoupal-test
KeyPair: AdvancedAdministrator
NumberOfTeams: 1

VPC: vpc-b97272dc
PublicRouteTable: rtb-c8c526ac
SecurityGroup: sg-adf2b9c9
Teams:

  Id: 0
  SubnetMask: 10.0.0.0/24
  LoadBalancer: dcoupal-t-OpsMgrLB-187Y2BIZ8ETKG-394908656.us-west-1.elb.amazonaws.com
  Hosts:
    Id: i-ce0e4a8b  Role: Node1     IP: 54.193.69.25    PrivateIP: 10.0.0.142
    Id: i-ab0c48ee  Role: OpsMgr1   IP: 54.67.73.218    PrivateIP: 10.0.0.145
    Id: i-cd0e4a88  Role: OpsMgr2   IP: 54.183.174.92   PrivateIP: 10.0.0.151
    Id: i-b40c48f1  Role: OpsMgr3   IP: 54.193.73.93    PrivateIP: 10.0.0.133

  Id: 1
  SubnetMask: 10.0.1.0/24
  LoadBalancer: dcoupal-t-OpsMgrLB-10CR1BLJEC2CK-3078954.us-west-1.elb.amazonaws.com
  Hosts:
    Id: i-6a0d492f  Role: Node1     IP: 52.53.244.51    PrivateIP: 10.0.1.211
    Id: i-6b0d492e  Role: OpsMgr1   IP: 54.193.40.211   PrivateIP: 10.0.1.238
    Id: i-690d492c  Role: OpsMgr2   IP: 54.183.192.16   PrivateIP: 10.0.1.9
    Id: i-690c482c  Role: OpsMgr3   IP: 54.193.59.211   PrivateIP: 10.0.1.202
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
      help="File in which to store the output")

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
