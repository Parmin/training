#! /usr/bin/env python

import logging
import argparse
import sys
from datetime import date,timedelta
import time
from provisioner import Provisioner
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

    parser.add_argument('--teams', dest='teams', required=True, type=int,
    help='Number of teams for this training run', choices=range(1,5))

    parser.add_argument('--profile', dest='awsprofile', default='default',
    type=str, help='AWS profile that will launch the environment')

    parser.add_argument('--duration', dest='duration', default=3,
    type=int, help="Duration of the training run in days")

    parser.add_argument('--dir', dest='dir', default=".",
    type=str, help="Output build directory path")

    parser.add_argument('--instances', dest='instances', default=16, type=int,
    help="Number of instances per team")

    args = parser.parse_args()
    logger.info("Collected the following arguments {0}".format(args))

    training_run = args.training_run
    awsprofile = args.awsprofile

    logger.debug("Going to deploy new traing run")
    end_date = date.today()+timedelta(days=args.duration)

    logger.debug("Training will finish {:%d, %b %Y}".format(end_date))

    pr = Provisioner(training_run, end_date=end_date, aws_profile=awsprofile,
        teams=args.teams)

    pr.connect()
    build_id = date.today().strftime("%Y-%m-%d:%H:%M:%S")
    logger.debug("Building {0} stack".format(build_id))
    pr.basedir = args.dir
    pr.number_of_instances = args.instances
    pr.build(build_id, False)
    logger.debug("All teams:".format(pr.teams))



if __name__ == "__main__":
    main()