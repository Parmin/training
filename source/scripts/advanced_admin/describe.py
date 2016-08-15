#! /usr/bin/env python

# Issues:

# TODO
#   - add a 'format=json' mode, for other scripts to query the file to modify/terminate instances.

import logging
import argparse
import sys
from datetime import date,timedelta
import time
from provisioner_aws_cf import Provisioner_aws_cf
from provisioner_aws_plain import Provisioner_aws_plain

FORMAT = '%(asctime)-15s %(message)s'

def setup_logging(logger):
    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setLevel(logging.DEBUG)
    consoleHandler.setFormatter(logging.Formatter(FORMAT))

    logger.addHandler(consoleHandler)
    logger.setLevel(logging.DEBUG)

def main():
    logger = logging.getLogger(__name__)
    setup_logging(logger)

    parser = argparse.ArgumentParser(description='Deploy AWS training environment')
    parser.add_argument('--run', dest='training_run', required=True,
    help='environment training run identifier', type=str)

    parser.add_argument('--profile', dest='awsprofile', default='default',
    type=str, help='AWS profile that will launch the environment')

    parser.add_argument('--provider', dest='provider', default="aws-cf", type=str,
    help="Provider, one of 'aws-cf' or 'aws-plain'")

    parser.add_argument('--verbose', dest='verbose', action='store_true',
      help="Show more details in the output")

    args = parser.parse_args()
    logger.info("Collected the following arguments {0}".format(args))

    training_run = args.training_run
    awsprofile = args.awsprofile

    if args.provider == "aws-cf":
        pr = Provisioner_aws_cf(args, training_run, aws_profile=awsprofile)
    elif args.provider == "aws-plain":
        pr = Provisioner_aws_plain(training_run, aws_profile=awsprofile)
    else:
        print("FATAL - invalid provider, must be 'aws-plain' or 'aws-cf' " % args.provider)
        sys.exit(1)

    pr.connect()
    build_id = date.today().strftime("%Y-%m-%d:%H:%M:%S")
    logger.debug("Describing run: {0}".format(training_run))
    pr.describe()


if __name__ == "__main__":
    main()
