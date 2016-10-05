#! /usr/bin/env python

# Issues:
#   - when running command the first time you may:
#     a) be asked to add the host to 'known_host'
#     b) not a) because you have the setting 'StrictHostKeyChecking no' in your '/etc/ssh/ssh_config'
#        however, you will have an error if the first time is trying to run a local script, as 'scp'
#        will not add the host, but the second run will work, or a first pass with a cmd will also set things right
#   - should we run the commands/scripts in parallel with workers, or sequentially, or have it as an option?

# TODO
#   - once we support commands, we may want to support passing options to them
#   - support file names with spaces in them?
#   - allow to use a cached .json file (from describe) to avoid describing the stacks again, which is slow
#   - support regex in list of hosts to run cmd/script on

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
    parser.add_argument('--cmd', dest='cmd', type=str,
      help="remote cmd to execute on the selected hosts. May need to quote the command")

    parser.add_argument('--etchosts', dest='etchosts', action='store_true',
      help="Create a 'hosts' file for each team and upload them into /tmp. You still need to add the info in '/etc/hosts'")

    parser.add_argument('--ips', dest='ips', type=str,
      help="List of IPs for which the instances are considered")

    parser.add_argument('--out', dest='out', type=str,
      help="File in which to store the output, NOT IMPLEMENTED YET")

    parser.add_argument('--profile', dest='awsprofile', default='default', type=str,
      help="AWS profile that will launch the environment")

    parser.add_argument('--provider', dest='provider', default="aws-cf", type=str,
      help="Provider, one of 'aws-cf' or 'aws-plain'")

    parser.add_argument('--roles', dest='roles', type=str,
      help="List of roles (or regexes) to match the hosts to manage")

    parser.add_argument('--run', dest='training_run', type=str, required=True,
      help="environment training run identifier")

    parser.add_argument('--script', dest='script', type=str,
      help="local script to execute on the selected hosts. May need to quote the script")

    parser.add_argument('--teams', dest='teams', type=str,
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

    if args.cmd is None and args.script is None and args.etchosts is None:
      fatal(1, "You must provide a --cmd or a --script to execute on the remote hosts, or --etchosts")

    if (args.teams is None or args.roles is None) and args.ips is None:
      fatal(1, "You must provide either --teams/--roles or --ips to specify the hosts to consider")

    pr.connect()
    build_id = date.today().strftime("%Y-%m-%d:%H:%M:%S")
    logger.debug("Managing run: {0}".format(training_run))
    pr.manage(args.cmd, args.script)


if __name__ == "__main__":
    main()
