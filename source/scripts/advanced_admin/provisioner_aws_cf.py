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

    # TODO - cleanup the arguments to the constructor, maybe just keeping 'args'
    def __init__(self, args, training_run, aws_profile="default", teams=1, end_date=date.today()+timedelta(days=7), aws_region=None, keypair=None):
        self.training_run = training_run
        self.aws_profile = aws_profile
        self.number_of_teams = teams
        self.aws_region = aws_region
        self.end_date = end_date
        self.keypair = keypair
        self.args = args

        self.session = None
        self.client = None
        self.teams = []

    def build(self, build_id, dryrun=True):
        """
        Build the initial VPC with the team '0' in it, this team can be used for administrative purposes.
        """
        me = getpass.getuser()
        if dryrun:
            testmode = "true"
        else:
            testmode = "false"

        with open("advops-base_team.template", 'r') as f:
            response = self.client.create_stack(
	            StackName = self.training_run,
	            TemplateBody = f.read(),
	            Parameters = [
	                { "ParameterKey": "NbTeams", "ParameterValue": str(self.number_of_teams) },
	                { "ParameterKey": "KeyPair", "ParameterValue": self.keypair },
	                { "ParameterKey": "TestMode", "ParameterValue": testmode }
	            ],
	            # Add 'Project' and 'Expire-on'
	            Tags = [
	                { "Key": "Name", "Value": "AdvOps - " + self.training_run },
	                { "Key": "Owner", "Value": me },
	                { "Key": "Project", "Value": "AdvOps - " + self.training_run },
	                { "Key": "Expire-on", "Value": str(self.end_date) },
	                { "Key": "Run", "Value": self.training_run }
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

        run_resources = self.client.describe_stack_resources(StackName=self.training_run)
        runinfo = self._get_outputs_for_stack(self.training_run)
        print "Run: %s\n" % (self.training_run)
        print "  Key pair: %s" % (runinfo['KeyPair'])
        print "  Number of Teams: %s" % (runinfo['NbTeams'])
        print ""
        print "  VPC: %s" % (runinfo['VPC'])
        print "  Public Route Table: %s" % (runinfo['PublicRouteTable'])
        print "  Security Group: %s" % (runinfo['SSHandHTTPSecurityGroup'])
        # Describe all sub stacks, starting with the top one for the 'run'
        #MyPrettyPrinter().pprint(run_resources)
        for one_run_resource in run_resources['StackResources']:
            # Need VPC, key/pair, 
            if one_run_resource['ResourceType'] == 'AWS::CloudFormation::Stack':
                # This is one team
                physicalId = one_run_resource['PhysicalResourceId']
                teaminfo = self._get_outputs_for_stack(physicalId)
                if self.args.verbose:
                    print "\n  Team %s (%s)" % (one_run_resource['LogicalResourceId'], physicalId)
                    print   "    Subnet - Id: %s  Mask: %s" % (teaminfo['Subnet'], teaminfo['SubnetMask'])
                    print   "    LoadBalancer: %s" % (teaminfo['LoadBalancerHostName'])
                else:
                    print "\n  Team %s" % (teaminfo['TeamNumber'])
                    print   "    Subnet - Mask: %s" % (teaminfo['SubnetMask'])
                    print   "    LoadBalancer: %s" % (teaminfo['LoadBalancerHostName'])
                print ""
                # Getting all resources for the stack that created this team
                team_resources = self.client.describe_stack_resources(StackName=physicalId)
                for one_team_resource in team_resources['StackResources']:
                    # Need Instances, Load Balancer, subnet, team number
                    if one_team_resource['ResourceType'] == 'AWS::CloudFormation::Stack':
                        # Need Instance ID, IP, Role
                        physicalId = one_team_resource['PhysicalResourceId']
                        hostinfo = self._get_outputs_for_stack(physicalId)
                        hosttags = self._get_tags_for_stack(physicalId)
                        print "    Host - Id: %-11s  Role: %-10s  IP: %s" % (hostinfo['InstanceID'], hosttags['Role'], hostinfo['PublicIP'])
        print ""

    def destroy(self):
        """
        TODO: verify that the stack exists before trying to delete it
        """
        self.client.delete_stack(StackName = self.training_run)
        None

    def _get_outputs_for_stack(self, stackId):
        """
        Return a dictionary with all the 'outputs' for a given stack
        """
        stack_description = self.client.describe_stacks(StackName=stackId)
        outputs = stack_description['Stacks'][0]['Outputs']
        info = dict()
        for output in outputs:
            info[output['OutputKey']] = output['OutputValue']
        return info

    def _get_tags_for_stack(self, stackId):
        """
        Return a dictionary with all the 'outputs' for a given stack
        """
        stack_description = self.client.describe_stacks(StackName=stackId)
        outputs = stack_description['Stacks'][0]['Tags']
        info = dict()
        for output in outputs:
            info[output['Key']] = output['Value']
        return info

# Imported code
class MyPrettyPrinter(pprint.PrettyPrinter):
    def format(self, object, context, maxlevels, level):
        if isinstance(object, unicode):
            return (object.encode('utf8'), True, False)
        return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)
