#! /usr/bin/env python

# Issues
#   botocore.exceptions.ClientError: An error occurred (ValidationError) when calling the DeleteLoadBalancer operation: LoadBalancer name cannot contain characters that are not letters, or digits or the dash.

# TODO:
#   - warn if the run to delete does not exists in that region
#   - verify it deletes
#       - instances
#       - interfaces
#       - security group
#       - VPC
#       - load balancer
#       - key/pair
#   - should accumulate errors and continue instead of throwing an exception

from provisioner_aws_cf import Provisioner_aws_cf
import argparse
import logging
import sys

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

    parser = argparse.ArgumentParser(description='Deploy AWS training environment')
    parser.add_argument('--run', dest='training_run', required=True,
    help='environment training run identifier', type=str)

    parser.add_argument('--profile', dest='awsprofile', default='default',
    type=str, help='AWS profile that will launch the environment')

    parser.add_argument('--region', dest='awsregion', default='default', type=str,
      help="AWS region that is looked at")

    args = parser.parse_args()
    training_run = args.training_run
    awsprofile = args.awsprofile
    awsregion = args.awsregion

    pr = Provisioner_aws_cf(args, training_run, aws_profile=awsprofile, aws_region=awsregion)

    pr.connect()
    logger.info('Destroying {0}'.format(args.training_run))
    pr.destroy()

if __name__ == '__main__':

    main()
