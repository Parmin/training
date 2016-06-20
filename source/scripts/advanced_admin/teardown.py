#! /usr/bin/env python
from provisioner import Provisioner
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
    logger.info('Tearign Down Environment')

    parser = argparse.ArgumentParser(description='Deploy AWS training environment')
    parser.add_argument('--run', dest='training_run', required=True,
    help='environment training run identifier', type=str)

    parser.add_argument('--profile', dest='awsprofile', default='default',
    type=str, help='AWS profile that will launch the environment')

    args = parser.parse_args()

    pr = Provisioner(args.training_run, aws_profile=args.awsprofile)
    pr.connect()
    logger.info('Destroying {0}'.format(args.training_run))
    pr.destroy()

if __name__ == '__main__':

    main()
