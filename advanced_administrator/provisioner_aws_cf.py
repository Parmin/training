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
S3_FILES_PATH = os.path.join(os.path.dirname(__file__), "s3")

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
    def __init__(self, args, training_run, aws_profile="default", teams=1, end_date=date.today()+timedelta(days=7), aws_region="default", keypair=None):
        self.training_run = training_run
        self.aws_profile = aws_profile
        self.number_of_teams = teams
        self.aws_region = aws_region
        self.end_date = end_date
        self.keypair = keypair
        self.args = args

        self.session = None
        self.client = None
        self.ec2 = None
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

        if self.args.noom:
            ommode = "false"
        else:
            ommode = "true"

        # http://boto3.readthedocs.io/en/latest/reference/services/cloudformation.html#CloudFormation.Client.create_stack
        template_path = os.path.join(S3_FILES_PATH, "cf-templates", "advadmin-run.template")
        with open(template_path, 'r') as f:
            response = self.client.create_stack(
                StackName = self.training_run,
                TemplateBody = f.read(),
                OnFailure = 'DO_NOTHING',
                Parameters = [
                    { "ParameterKey": "NbTeams", "ParameterValue": str(self.number_of_teams) },
                    { "ParameterKey": "NbNodes", "ParameterValue": str(self.args.instances) },
                    { "ParameterKey": "KeyPair", "ParameterValue": self.keypair },
                    { "ParameterKey": "OMMode", "ParameterValue": ommode },
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
        # Need to wait on the completion of the above to extract few parameters to create the other teams?


    def build_team(self, build_id, vpc, team_id):
        None


    def connect(self):
        """
        Establish the resources and client objects
        """
        try:
            if self.aws_region != "default" and self.aws_region is not None:
                self.session = boto3.session.Session(region_name=self.aws_region)
            elif self.aws_profile != "default" and self.aws_profile is not None:
                self.session = boto3.session.Session(profile_name=self.aws_profile)
            else:
                self.session = boto3.session.Session()
            self.client = self.session.client('cloudformation')
            self.ec2 = self.session.client('ec2')
        except ProfileNotFound, e:
            fatal(1, "Could not find the AWS profile '{0}' \n".format(self.aws_profile) +
                "Check the ~/.aws/config file and/or configure with 'aws configure'")

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
            # TODO - remove all the files that would match this run, and for all teams
            (run_info, teams_info) = self.get_run_info(printit=True, perteam=True)
            if self.args.out:
                outfiles = self.args.out
            else:
                outfiles = "/tmp/" + self.training_run
            try:
                f = open(outfiles, 'w')
                contents = json.dumps(run_info, indent=2)
                f.write(contents + "\n")
                f.close()
                for key in teams_info.keys():
                    team_info = teams_info[key].get_dict()
                    f = open(outfiles + "-" + key, 'w')
                    contents = json.dumps(team_info, indent=2)
                    f.write(contents + "\n")
                    f.close()
            except Exception, e:
                fatal(1, e.__str__())
            print("\nJSON file for the above run has been saved in: {}".format(outfiles))
            print("There is also one file per team saved in: {}-<teamNumber>".format(outfiles))


    def destroy(self):
        """
        TODO: verify that the stack exists before trying to delete it
        """
        self.client.delete_stack(StackName = self.training_run)
        None

    def get_run_info(self, printit, perteam=False):
        run_info = BuildAndPrintDict(printit)
        teams_info = dict()

        # Can't describe a run in 'CREATE_IN_PROGRESS'
        run_description = self._describe_stack(self.training_run)
        if run_description['StackStatus'] == 'CREATE_IN_PROGRESS':
            fatal(1, "Can't describe a stack in 'CREATE_IN_PROGRESS' state")
        else:
            run_resources = self._describe_stack_resources(self.training_run)
            runinfo = self._get_outputs_for_stack(self.training_run)
            run_info.comment("")
            run_info.key_values(("Name", self.training_run))
            run_info.key_values(("KeyPair", runinfo['KeyPair']))
            run_info.key_values(("NumberOfTeams", runinfo['NbTeams']))
            run_info.comment("")
            run_info.start_list("Teams")
            # Describe all sub stacks, starting with the top one for the 'run'
            for one_run_resource in run_resources['StackResources']:
                # Need VPC, key/pair,
                if one_run_resource['ResourceType'] == 'AWS::CloudFormation::Stack':
                    # This is one team
                    one_team_info = BuildAndPrintDict(printit=False)
                    physicalId = one_run_resource['PhysicalResourceId']
                    teaminfo = self._get_outputs_for_stack(physicalId)
                    run_info.comment("")
                    run_info.new_list_obj()
                    run_info.key_values(("Id", teaminfo['TeamNumber']))
                    run_info.key_values(("LoadBalancer", teaminfo['LoadBalancerHostName']))
                    run_info.key_values(("SecurityGroup", teaminfo['SSHandHTTPSecurityGroup']))
                    run_info.key_values(("VPC", teaminfo['VPC']))
                    run_info.key_values(("SubnetMask", teaminfo['SubnetMask']))
                    # Keep also the info for the team
                    one_team_info.key_values(("Id", teaminfo['TeamNumber']))
                    one_team_info.key_values(("LoadBalancer", teaminfo['LoadBalancerHostName']))
                    one_team_info.key_values(("SecurityGroup", teaminfo['SSHandHTTPSecurityGroup']))
                    one_team_info.key_values(("VPC", teaminfo['VPC']))
                    one_team_info.key_values(("SubnetMask", teaminfo['SubnetMask']))
                    # Getting all resources for the stack that created this team
                    team_resources = self._describe_stack_resources(physicalId)
                    run_info.start_list("Hosts")
                    one_team_info.start_list("Hosts")
                    for one_team_resource in team_resources['StackResources']:
                        # Need Instances, Load Balancer, subnet, team number
                        if one_team_resource['ResourceType'] == 'AWS::CloudFormation::Stack':
                            # Need Instance ID, IP, Role
                            run_info.new_list_obj()
                            physicalId = one_team_resource['PhysicalResourceId']
                            hostinfo = self._get_outputs_for_stack(physicalId)
                            hosttags = self._get_tags_for_stack(physicalId)
                            run_info.key_values( ("Id", hostinfo['InstanceID'], "{:10}"), ("Role", hosttags['Role'], "{:8}") )
                            # If the machine rebooted, it would have a new public name and public IP
                            # ... so get the current info by querying the instance info directly
                            instanceinfo = self._get_instance_info(hostinfo['InstanceID'])
                            run_info.key_values( ("PrivateIP", instanceinfo['PrivateIP'], "{:15}"), ("PrivateName", instanceinfo['PrivateDnsName'], "{:50}") )
                            run_info.key_values( ("PublicIP", instanceinfo['PublicIP'], "{:15}"), ("PublicName", instanceinfo['PublicDnsName'], "{:50}") )
                            run_info.comment("")
                            # Doing the same for the team
                            one_team_info.new_list_obj()
                            one_team_info.key_values( ("Id", hostinfo['InstanceID'], "{:10}"), ("Role", hosttags['Role'], "{:8}") )
                            one_team_info.key_values( ("PrivateIP", instanceinfo['PrivateIP'], "{:15}"), ("PrivateName", instanceinfo['PrivateDnsName'], "{:50}") )
                            one_team_info.key_values( ("PublicIP", instanceinfo['PublicIP'], "{:15}"), ("PublicName", instanceinfo['PublicDnsName'], "{:50}") )
                    run_info.end_list("Hosts")
                    one_team_info.end_list("Hosts")
                    teams_info[teaminfo['TeamNumber']] = one_team_info
            run_info.end_list("Teams")
            run_info.comment("")
        return(run_info.get_dict(), teams_info)

    def manage(self, cmd, script):
        """
        Execute something on a bunch of hosts
        """
        etchosts_filename = "/tmp/hosts"
        # Get the list of hosts from the deployment
        if self.args.info is None:
            (run_info, _) = self.get_run_info(printit=False, perteam=False)
        else:
            print("Loading cached information from {}".format(self.args.info))
            with open(self.args.info) as json_data:
                run_info = json.load(json_data)

        # With the info about the run, let's take the actions on the desired hosts
        keypair = run_info['KeyPair']
        for team in run_info['Teams']:
            if (self.args.ips is not None) or (self.args.teams == "all") or (self.args.teams is not None and team['Id'] in self.args.teams):
                print("\nTeam {}".format(team['Id']))
                if self.args.etchosts is not None:
                    etchosts_file = open(etchosts_filename, 'w')
                for host in team['Hosts']:
                    if (self.args.ips is not None and host['PublicIP'] in self.args.ips) or (self.args.roles == "all") or (self.args.roles is not None and host['Role'] in self.args.roles):
                        print("\n  {:14}  {}".format(host['PublicIP'], host['Role']))
                        # Is this a script to upload?
                        if cmd is not None:
                            # Run the remote command
                            self._run_cmd_on_host(host['PublicIP'], cmd, keypair)
                        elif script is not None:
                            # Upload the script ant run it
                            remote_script = self._transfer_file_to_host(host['PublicIP'], script, keypair)
                            self._run_cmd_on_host(host['PublicIP'], "bash " + remote_script, keypair)
                    if self.args.etchosts is not None:
                        etchosts_file.write("{:14}   {}\n".format(host['PrivateIP'], host['Role']))
                if self.args.etchosts is not None:
                    etchosts_file.close()
                    self._transfer_file_to_host(host['PublicIP'], etchosts_filename, keypair)

    def _get_instance_info(self, instanceId):
        """
        Return a dictionary with some of the 'instance attributes' for a given EC2 instance
        """
        info = dict()
        instance = self.ec2.describe_instances(InstanceIds=[instanceId])
        instance_info = instance['Reservations'][0]['Instances'][0]
        # If the instance is stopped, it will not have a publicIP
        if instance_info.has_key('PublicIpAddress'):
            info['PublicIP'] = instance_info['PublicIpAddress']
        else:
            info['PublicIP'] = ''
        if instance_info.has_key('PublicDnsName'):
            info['PublicDnsName'] = instance_info['PublicDnsName']
        else:
            info['PublicDnsName'] = ''
        info['PrivateIP'] = instance_info['PrivateIpAddress']
        info['PrivateDnsName'] = instance_info['PrivateDnsName']
        return info

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
