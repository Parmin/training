# Class to provision training classes, using AWS Cloud Formation

import boto3
from botocore.exceptions import *
from datetime import date, timedelta
import getpass
import pprint
import simplejson as json

class Provisioner_aws_cf(object):
    """
    Class for provisioning management of Training Environment, using basic AWS artifacts

    TODO
    - add expiration date on artifacts
    - name the Load Balancer, however we are limited to 32 chars. Right solution would be "LB-<run>-<team>"
    - name the stacks without the generated part from CF. Right solution would be "<run>-<team>-<host>"
    - attach Elastic IP to LoadBalancer?
    """

    def __init__(self, training_run, aws_profile="default", teams=1, end_date=date.today()+timedelta(days=7), aws_region=None):
        self.training_run = training_run
        self.aws_profile = aws_profile
        self.number_of_teams = teams
        self.aws_region = aws_region
        self.end_date = end_date
        self.session = None
        self.client = None
        self.teams = []

    def build(self, build_id, dryrun=True):
        """
        Build the initial VPC with the team '0' in it, this team can be used for administrative purposes.
        """
        me = getpass.getuser()
        with open("advops-base_team.template", 'r') as f:
            response = self.client.create_stack(
	            StackName = self.training_run,
	            TemplateBody = f.read(),
	            Parameters = [
	                { "ParameterKey": "NbTeams", "ParameterValue": str(self.number_of_teams) },
	                { "ParameterKey": "KeyPair", "ParameterValue": "AdvancedOpsTraining" }
	            ],
	            Tags = [
	                { "Key": "Name", "Value": "AdvOps - " + self.training_run },
	                { "Key": "Run", "Value": self.training_run },
	                { "Key": "Owner", "Value": me }
	            ]
	        )
        # Need to wait on the completion of the above to extract few parameters to create the other teams


    def build_team(self, build_id, vpc, team_id):
        None


    def connect(self):
        """
        Establish the resources and client objects
        """
        try:
            if self.aws_region is None:
                self.session = boto3.session.Session(profile_name=self.aws_profile)
            else:
                self.session = boto3.session(profile_name=self.aws_profile, aws_region=self.aws_region)
            self.client = self.session.client('cloudformation')
        except ProfileNotFound, e:
            log.error("\nFATAL - Could not find the AWS profile '{0}'".format(self.aws_profile))
            log.error("Check the ~/.aws/config file and/or configure with 'aws configure'")
            sys.exit(1)

    def describe(self):

        # TODO - check if the stack exists
        response = self.client.describe_stacks(StackName=self.training_run)
        #MyPrettyPrinter().pprint(response)

        # Describe all sub stacks, starting with the top one for the 'run'
        run_resources = self.client.describe_stack_resources(StackName=self.training_run)
        MyPrettyPrinter().pprint(run_resources)
        for one_run_resource in run_resources['StackResources']:
            if one_run_resource['ResourceType'] == 'AWS::CloudFormation::Stack':
                # This is one team
                print "  Team: " + one_run_resource['LogicalResourceId']
                team_resources = self.client.describe_stack_resources(PhysicalResourceId=one_run_resource['PhysicalResourceId'])
                MyPrettyPrinter().pprint(team_resources)
                for one_team_resource in team_resources['StackResources']:
                    if one_team_resource['ResourceType'] == 'AWS::CloudFormation::Stack':
                        print "    Host:"

    def destroy(self):
    	"""
    	TODO: verify that the stack exists before trying to delete it
    	"""
        self.client.delete_stack(StackName = self.training_run)
        None

class MyPrettyPrinter(pprint.PrettyPrinter):
    def format(self, object, context, maxlevels, level):
        if isinstance(object, unicode):
            return (object.encode('utf8'), True, False)
        return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)
