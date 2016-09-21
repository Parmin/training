#! /usr/bin/env python

# Issues:
#   - should we run the commands/scripts in parallel with workers, or sequentially, or have it as an option?

# TODO
#   - allow to run commands on a list of IPs instead of roles/teams
#   - once we support commands, we may want to support passing options to them

"""
Example:

$ ./manage.py --profile training-west --run dcoupal-test --teams 0,1 --roles OpsMgr1,OpsMgr2 --cmd "/bin/hostname -f"

Team 0
  54.183.172.229  OpsMgr1
ip-10-0-0-47.us-west-1.compute.internal

  54.67.126.74    OpsMgr2
ip-10-0-0-10.us-west-1.compute.internal

Team 1
  54.183.194.222  OpsMgr1
ip-10-0-1-161.us-west-1.compute.internal

  52.53.252.177   OpsMgr2
ip-10-0-1-160.us-west-1.compute.internal
"""

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

    parser = argparse.ArgumentParser(description='Helper to manage a set of hosts and run commands on them')
    parser.add_argument('--cmd', dest='cmd', type=str, required=True,
      help="cmd or script to execute on the selected hosts. May need to quote the command")

    parser.add_argument('--run', dest='training_run', type=str, required=True,
      help="environment training run identifier, or none to see all the runs")

    parser.add_argument('--out', dest='out', type=str,
      help="File in which to store the output")

    parser.add_argument('--profile', dest='awsprofile', default='default', type=str,
      help="AWS profile that will launch the environment")

    parser.add_argument('--provider', dest='provider', default="aws-cf", type=str,
      help="Provider, one of 'aws-cf' or 'aws-plain'")

    parser.add_argument('--roles', dest='roles', type=str, required=True,
      help="List of roles (or regexes) to match the hosts to manage")

    parser.add_argument('--teams', dest='teams', type=str, required=True,
      help="List of teams for which the instances are considered (0,1,...). Use 'all' for all of them")

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
    logger.debug("Managing run: {0}".format(training_run))
    pr.manage(args.cmd)


if __name__ == "__main__":
    main()
