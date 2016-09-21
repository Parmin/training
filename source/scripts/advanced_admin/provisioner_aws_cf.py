# Class to provision training classes, using AWS Cloud Formation

import boto3
from botocore.exceptions import *
from datetime import date, timedelta
import getpass
import os
import os.path
import re
import simplejson as json
import subprocess
import sys

from provider_utils import *

TOP_STACK_DESC = "This is the top stack template to create a training class"

class Provisioner_aws_cf(object):
    """
    Class for provisioning management of Training Environment, using basic AWS artifacts

    TODO
    - nice error message if we run over the limit of instances
    - check if the run exists (done for describe, needed for deploy and teardown)
    - check if run is 'completed' in order to report info?
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

        with open("s3/cf-templates/advadmin-base_team.template", 'r') as f:
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
        if self.training_run is None:
            # No run specified, list all of them.
            # Beware that AWS does page the results
            more_results = True
            next_token = None
            print("")
            print("{:20} {:20} {}".format('Stack Name', 'Stack Status', 'Creation Time'))
            while more_results:
                if next_token:
                    stack_list  = self.client.list_stacks(NextToken=next_token)
                else:
                    stack_list  = self.client.list_stacks()
                for one_stack in stack_list['StackSummaries']:
                    if self.args.verbose or (one_stack.has_key('TemplateDescription') and re.match(TOP_STACK_DESC, one_stack['TemplateDescription']) and one_stack['StackStatus'] not in ['DELETE_COMPLETE']):
                        print("{:20} {:20} {}".format(one_stack['StackName'], one_stack['StackStatus'], one_stack['CreationTime']))
                if stack_list.has_key('NextToken'):
                    next_token = stack_list['NextToken']
                else:
                    more_results = False
        else:
            run_info = self.get_run_info(printit=True)
            if self.args.out:
                try:
                    f = open(self.args.out, 'w')
                    contents = json.dumps(run_info, indent=2)
                    f.write(contents + "\n")
                    f.close()
                except Exception, e:
                    fatal(1, e.__str__())
                print("\nJSON file for the above has been saved in: {}".format(self.args.out))

    def destroy(self):
        """
        TODO: verify that the stack exists before trying to delete it
        """
        self.client.delete_stack(StackName = self.training_run)
        None

    def get_run_info(self, printit):
        run_info = BuildAndPrintDict(printit)

        run_description = self._describe_stack(self.training_run)
        run_resources = self._describe_stack_resources(self.training_run)
        runinfo = self._get_outputs_for_stack(self.training_run)
        run_info.comment("")
        run_info.key_values(("Name", self.training_run))
        run_info.key_values(("KeyPair", runinfo['KeyPair']))
        run_info.key_values(("NumberOfTeams", runinfo['NbTeams']))
        run_info.comment("")
        run_info.key_values(("VPC", runinfo['VPC']))
        run_info.key_values(("PublicRouteTable", runinfo['PublicRouteTable']))
        run_info.key_values(("SecurityGroup", runinfo['SSHandHTTPSecurityGroup']))
        run_info.start_list("Teams")
        # Describe all sub stacks, starting with the top one for the 'run'
        for one_run_resource in run_resources['StackResources']:
            # Need VPC, key/pair, 
            if one_run_resource['ResourceType'] == 'AWS::CloudFormation::Stack':
                # This is one team
                physicalId = one_run_resource['PhysicalResourceId']
                teaminfo = self._get_outputs_for_stack(physicalId)
                run_info.comment("")
                run_info.new_list_obj()
                run_info.key_values(("Id", teaminfo['TeamNumber']))
                run_info.key_values(("SubnetMask", teaminfo['SubnetMask']))
                run_info.key_values(("LoadBalancer", teaminfo['LoadBalancerHostName']))
                # Getting all resources for the stack that created this team
                team_resources = self._describe_stack_resources(physicalId)
                run_info.start_list("Hosts")
                for one_team_resource in team_resources['StackResources']:
                    # Need Instances, Load Balancer, subnet, team number
                    if one_team_resource['ResourceType'] == 'AWS::CloudFormation::Stack':
                        # Need Instance ID, IP, Role
                        run_info.new_list_obj()
                        physicalId = one_team_resource['PhysicalResourceId']
                        hostinfo = self._get_outputs_for_stack(physicalId)
                        hosttags = self._get_tags_for_stack(physicalId)
                        run_info.key_values( ("Id", hostinfo['InstanceID'], "{:10}"), ("Role", hosttags['Role'], "{:8}"), ("IP", hostinfo['PublicIP'], "{:14}"), ("PrivateIP", hostinfo['PrivateIP'], "{:14}") )
                run_info.end_list("Hosts")
        run_info.end_list("Teams")
        run_info.comment("")
        return run_info.get_dict()

    def manage(self, cmd):
        """
        Execute something on a bunch of hosts
        """
        # Get the list of hosts from the deployment
        run_info = self.get_run_info(printit=False)
        keypair = run_info['KeyPair']
        for team in run_info['Teams']:
            if self.args.teams == "all" or team['Id'] in self.args.teams:
                print("\nTeam {}".format(team['Id']))
                for host in team['Hosts']:
                    if self.args.roles == "all" or host['Role'] in self.args.roles:
                        print("\n  {:14}  {}".format(host['IP'], host['Role']))
                        # Is this a script to upload?
                        if os.path.isfile(cmd):
                            # upload the file
                            remote_script = self._transfer_file_to_host(host['IP'], cmd, keypair)
                            self._run_cmd_on_host(host['IP'], "bash " + remote_script, keypair)
                        else:
                            self._run_cmd_on_host(host['IP'], cmd, keypair)

    def _get_outputs_for_stack(self, stackId):
        """
        Return a dictionary with all the 'outputs' for a given stack
        """
        info = dict()
        stack_description = self._describe_stack(stackId)
        if stack_description.has_key('Outputs'):
            outputs = stack_description['Outputs']
            for output in outputs:
                info[output['OutputKey']] = output['OutputValue']
        elif stack_description['StackStatus'] == 'ROLLBACK_COMPLETE':
            fatal(1, "The stack {} has errors or is not ready, the status is: {}".format(stackId, stack_description['StackStatus']))
        return info

    def _describe_stack(self, stackname):
        got_stack = False
        stack_description = {}
        try:
            stack_descriptions  = self.client.describe_stacks(StackName=stackname)
            for one_stack_description in stack_descriptions['Stacks']:
                if one_stack_description['StackName'] == stackname or one_stack_description['StackId'] == stackname:
                    got_stack = True
                    stack_description = one_stack_description
                    if self.args.verbose:
                        MyPrettyPrinter().pprint(one_stack_description)
                    break
        except ClientError, e:
            fatal(1, "ERROR - can't find the stack: {}".format(stackname))
        return stack_description

    def _describe_stack_resources(self, stackname):
        stack_resources  = self.client.describe_stack_resources(StackName=stackname)
        if self.args.verbose:
            MyPrettyPrinter().pprint(stack_resources)
        return stack_resources

    def _get_tags_for_stack(self, stackId):
        """
        Return a dictionary with all the 'outputs' for a given stack
        """
        stack_description = self._describe_stack(stackId)
        outputs = stack_description['Tags']
        info = dict()
        for output in outputs:
            info[output['Key']] = output['Value']
        return info

    def _run_cmd_on_host(self, host, cmd, pemfilename):
        """
        Run a command or script on a given host
        TODO - do not hardcode the user account 'centos'
               if file instead of command, upload the file on the host, then run it
        """
        ssh = subprocess.Popen(["ssh", "-i", os.environ['HOME'] + "/.ssh/" + pemfilename + ".pem", "-l", "centos", host, cmd],
                       shell=False,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
        result = ssh.stdout.readlines()
        error = ssh.stderr.readlines()
        if error:
            print("ERROR running the provided 'cmd': {}".format(cmd))
            for line in error:
                print line,
        else:
            for line in result:
                print line,

    def _transfer_file_to_host(self, host, file, pemfilename):
        """
        Upload a file on a given host
        TODO - do not hardcode the user account 'centos'
               if file instead of command, upload the file on the host, then run it
        """
        target_filename = os.path.join("/tmp", os.path.basename(file))
        ssh = subprocess.Popen(["scp", "-i", os.environ['HOME'] + "/.ssh/" + pemfilename + ".pem", file, "centos@" + host + ":" + target_filename],
                       shell=False,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
        result = ssh.stdout.readlines()
        error = ssh.stderr.readlines()
        if error:
            print("ERROR transfering the script to {}".format(host))
            for line in error:
                print line,
        else:
            for line in result:
                print line,
        return target_filename






