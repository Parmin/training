#! /usr/bin/env python

# Issues:
#   botocore.exceptions.ClientError: An error occurred (AuthFailure) when calling the RunInstances operation: Not authorized for images: [ami-12cb8f72]
#   => solved by having profile for TSE and profile for education
#
#   Could not create load balancer: An error occurred (ValidationError) when calling the CreateLoadBalancer operation: LoadBalancer name cannot contain characters that are not letters, or digits or the dash.
#
#   Could not register instances with load balancer DC_TEST-1-lb due to An error occurred (ValidationError) when calling the RegisterInstancesWithLoadBalancer operation: LoadBalancer name cannot contain characters that are not letters, or digits or the dash.
#
#   Missing required parameter in input: "LoadBalancerName" Unknown parameter in input: "LoadBlancerName", must be one of: LoadBalancerName, HealthCheck
#
#   Exception: No Public Instance Set Yet!
#
# TODOs:
#   - simpler error message when trying to create a run that already exists
#   - may want to push a '/etc/hosts' file on hosts to make it easier to go between each other?
#   - flag to not rollback the Stacks upon errors --debug
#   - better logging, it looks like everything is logged twice on the screen
#   - would like to check for return codes from creating the stacks, however the call is not blocking on the execution
#   - run mdiags on instances
#   - incorporate Ansible scripts
#   - consider terraform as an additional provider, or even replacement for CF
#   - Stacks:
#     - provision 2 disks per instance, for few data nodes
#   - validate names, can't have a '_' in them, use a '-'
#   - new command "manage" to run commands on different hosts
#   - document disabling rollbacks for debugging
#   - running out of instances?
#     - under 'events' for the instance stack, you will see: "Your quota allows for 0 more running instance(s). You requested at least 1"
#     - describe-stack-resources => "StackResources" => "ResourceStatus": "CREATE_FAILED" and "ResourceStatusReason": "Your quota allows for 0 more running instance(s). You requested at least 1"
#   - add the ability to pick different scripts to run per type of lab,
#     basically a concept of 'lab type' or config that may include the number of instances, ...

import logging
import argparse
import sys
from datetime import date,timedelta
import time
from provisioner_aws_cf import Provisioner_aws_cf

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

    parser.add_argument('--duration', dest='duration', default=3,
      type=int, help="Duration of the training run in days")

    parser.add_argument('--keypair', dest='keypair', default="AdvancedAdministrator", type=str,
      help="SSH keys to use. It defaults to 'AdvancedAdministrator'. You can provide another string, but the keys must exist under your account")

    parser.add_argument('--instances', dest='instances', default=12, type=int,
      help="Number of 'nodeX' instances per team, default is 12")

    parser.add_argument('--noom', dest='noom', action='store_true', default=False,
      help="Don't create the Ops Manager artifacts")

    parser.add_argument('--profile', dest='awsprofile', default='default',
      type=str, help='AWS profile that will launch the environment')

    parser.add_argument('--region', dest='awsregion', default='default', type=str,
      help="AWS region that is looked at")

    parser.add_argument('--run', dest='training_run', required=True, type=str,
      help='environment training run identifier')

    parser.add_argument('--teams', dest='teams', required=True, type=int, choices=range(1,16),
      help='Number of teams for this training run. Maximum is 15')

    parser.add_argument('--testmode', dest='testmode', action='store_true',
      help="Run in test mode, using less and smaller instances")

    args = parser.parse_args()
    logger.info("Collected the following arguments {0}".format(args))

    training_run = args.training_run
    awsprofile = args.awsprofile
    awsregion = args.awsregion
    if args.testmode == True and args.instances == 12:
        args.instances = 1

    logger.debug("Going to deploy new traing run")
    end_date = date.today()+timedelta(days=args.duration)

    logger.debug("Training will finish {:%d, %b %Y}".format(end_date))

    pr = Provisioner_aws_cf(args, training_run, end_date=end_date, aws_profile=awsprofile, aws_region=awsregion, teams=args.teams, keypair=args.keypair)

    if "_" in args.training_run:
        # since we use the name in the template name, it would not be accepted by AWS
        fatal(1, "Can't use '_' in the training run name due to a restriction in AWS")

    pr.connect()
    build_id = date.today().strftime("%Y-%m-%d:%H:%M:%S")
    logger.debug("Building {0} stack".format(build_id))
    pr.number_of_instances = args.instances
    pr.build(build_id, args.testmode)
    logger.debug("All teams:".format(pr.teams))
    print("It takes about 10 minutes to create the instances")
    print("You can get the overall status by running:")
    print("   describe.py --profile <AWS_training_profile>  -run <myrun>")
    print("OR using the 'CloudFormation' UI in AWS to see the progression of each stack and sub-stack")



if __name__ == "__main__":
    main()
