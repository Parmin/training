#! /usr/bin/env python

# Issues
#   botocore.exceptions.ClientError: An error occurred (ValidationError) when calling the DeleteLoadBalancer operation: LoadBalancer name cannot contain characters that are not letters, or digits or the dash.

# TODO:
#   - verify it deletes
#       - instances
#       - interfaces
#       - security group
#       - VPC
#       - load balancer
#       - key/pair
#   - should accumulate errors and continue instead of throwing an exception

from provisioner_aws_cf import Provisioner_aws_cf
from provisioner_aws_plain import Provisioner_aws_plain
import argparse
import logging
import sys

FORMAT = '%(asctime)-15s %(message)s'
consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setLevel(logging.DEBUG)
consoleHandler.setFormatter(logging.Formatter(FORMAT))
logger = logging.getLogger(__name__)
logger.addHandler(consoleHandler)
logger.setLevel(logging.DEBUG)

def main():
    logger.info('Tearing Down Environment')

    parser = argparse.ArgumentParser(description='Deploy AWS training environment')
    parser.add_argument('--run', dest='training_run', required=True,
    help='environment training run identifier', type=str)

    parser.add_argument('--profile', dest='awsprofile', default='default',
    type=str, help='AWS profile that will launch the environment')

    parser.add_argument('--provider', dest='provider', default="aws-cf", type=str,
    help="Provider, one of 'aws-cf' or 'aws-plain'")

    args = parser.parse_args()
    training_run = args.training_run
    awsprofile = args.awsprofile

    if args.provider == "aws-cf":
        pr = Provisioner_aws_cf(training_run, aws_profile=awsprofile)
    elif args.provider == "aws-plain":
        pr = Provisioner_aws_plain(training_run, aws_profile=awsprofile)
    else:
        print("FATAL - invalid provider, must be 'aws-plain' or 'aws-cf' " % args.provider)
        sys.exit(1)

    pr.connect()
    logger.info('Destroying {0}'.format(args.training_run))
    pr.destroy()

if __name__ == '__main__':

    main()
