import boto3
import botocore.exceptions
import logging
import iptools
import time
import os
import sys
from datetime import date, timedelta
FORMAT = '%(asctime)-15s %(message)s'
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logging.basicConfig(format=FORMAT)
module_logger = logging.getLogger(__name__)

class Team(object):

    def __init__(self, team_id, cidr_block):
        """
        Class that manages created teams
        """
        self.team_id = team_id
        self.cidr_block = cidr_block
        self._instances = []

    @property
    def team_id(self):
        return self._id

    @team_id.setter
    def team_id(self, team_id):
        if not team_id: raise Exception("team_id cannot be empty")
        self._id = team_id

    @property
    def cidr_block(self):
        return self._cidr_block

    @cidr_block.setter
    def cidr_block(self, cidr_block):
        self._cidr_block = cidr_block

    def append_instance(self, instance):
        if not instance: raise Exception("Cannot append empty instance")
        self._instances.append(instance)

    def generate_ip(self):
        rl = iptools.IpRangeList(self.cidr_block)
        for ip in rl:
            yield ip

class Provisioner(object):
    """
    Class for provisioning management of Training Environment
    """

    def __init__(self, training_run, aws_profile="default", teams=1,
        end_date=date.today()+timedelta(days=7), aws_region=None):
        self.training_run = training_run
        self.aws_profile = aws_profile
        self.number_of_teams = teams
        self._aws_region = aws_region
        self.end_date = end_date
        self._session = None
        self._client = None
        self._ec2 = None
        self._logger = logging.getLogger("Provisioner")
        self.cidr_block = '27.0.17.0/24'
        self._subnet_cidrblocks = [
            "27.0.17.0/27",
            "27.0.17.32/27",
            "27.0.17.64/27",
            "27.0.17.96/27",
            "27.0.17.128/27"]
        self.teams = []
        self._basedir = "."
        self.number_of_instances = 16
        self.instance_type = 'm3.xlarge'
        self.image_id = "ami-d63cccbb"

    @property
    def instance_type(self):
        return self._instance_type

    @instance_type.setter
    def instance_type(self, it):
        self._instance_type = it

    @property
    def teams(self):
        return self._teams

    @teams.setter
    def teams(self, teams):
        self._teams = teams

    @property
    def vpc(self):
        return self._vpc

    @vpc.setter
    def vpc(self, vpc):
        if not vpc : raise Exception('Vpc cannot be None')
        self._vpc = vpc

    @property
    def client(self):
        if not self._client: raise Exception('Client cannot be None')
        return self._client

    @client.setter
    def client(self, c):
        if not c: raise Exception('Client cannot be None')
        self._client = c

    @property
    def cidr_block(self):
        return self._cidr

    @cidr_block.setter
    def cidr_block(self, cidr):
        if not iptools.ipv4.validate_cidr(cidr): raise Exception('Incorrect CIDR BLOCK %s' % (cidr))
        self._cidr = cidr

    @property
    def training_run(self):
        self._logger.debug("get training_run: %s", self._training_run)
        return self._training_run

    @training_run.setter
    def training_run(self, tr):
        if not tr: raise Exception("training_run cannot be empty")
        self._training_run = tr

    @property
    def aws_profile(self):
        return self._awsp

    @aws_profile.setter
    def aws_profile(self, p):
        if not p: raise Exception("aws_profile cannot be empty")
        self._awsp = p

    @property
    def number_of_teams(self):
        return self._nteams

    @number_of_teams.setter
    def number_of_teams(self, n):
        if 10 > n < 1: raise Exception("Incorrect number of teams. Needs to be more than one and less than 10")
        self._nteams = n

    @property
    def end_date(self):
        self._logger.debug("get end_date: %s", self.training_run)
        return self._edate

    @end_date.setter
    def end_date(self, d):
        if  date.today() > d or d > date.today()+timedelta(days=30) : raise Exception("end_date %s cannot be before today or set for more than 30 days: %s " % (d, date.today()))
        self._edate = d

    @property
    def session(self):
        if not self._session: raise Exception("Session cannot be None")
        self._logger.debug("get session: %s", self.training_run)
        return self._session

    @session.setter
    def session(self, s):
        if not s: raise Exception("Session cannot be None")
        self._session = s

    @property
    def ec2(self):
        if not self._ec2: raise Exception("EC2 resource cannot be empty. Don't forget to connect()!")
        return self._ec2

    @ec2.setter
    def ec2(self, e):
        if not e: raise Exception("EC2 resource cannot be empty. Don't forget to connect()!")
        self._ec2 = e

    def connect(self):
        """
        Establish the resources and client objects
        """
        self.session = boto3.session.Session(profile_name=self.aws_profile) if self._aws_region is None else boto3.session(profile_name=self.aws_profile, aws_region=self._aws_region)
        self.ec2 = self.session.resource('ec2')
        self.client = self.session.client('ec2')

    def get_default_tags(self):
        return [
            {'Key': 'Name', 'Value': self.training_run},
            {'Key': 'Owner', 'Value': 'Advanced Training'},
            {'Key': 'Expire', 'Value': self.end_date.strftime("%s")}
            ]


    def add_tags_resource(self, resource, build_id, tags=[], statefull=True):
        """
        Adds all required tags for AWS account management:
        - Name: training_run
        - expires: end_date
        - Owner: "Advanced Training"

        """
        tags += self.get_default_tags()
        tags.append({
            "Key": "BUILDID",
            "Value": build_id
         })

        self._logger.info(
        "Adding tags %s to resource %s " % (str(tags), resource.id ))
        c = 5
        if statefull:
            while resource.state != "available" or c > 0:
                self._logger.info(
                "Resource {0} not yet available - current state {1}".format(
                resource.id, resource.state))
                time.sleep(1)
                c=c-1
                resource.reload()
        resource.create_tags(Tags=tags)

    def create_internet_gateway(self, build_id, vpc_id):
        self._logger.info(
        "Creating Internet Gateway for {0} on vpc {1}".format(build_id, vpc_id))
        response = self.client.create_internet_gateway()

        ig = self.ec2.InternetGateway(response['InternetGateway']['InternetGatewayId'])

        retries = 2
        while retries > 0 :
            try:
                retries-=1
                self.add_tags_resource(ig, build_id, [{'Key': 'VpcId', 'Value': vpc_id}], False)
            except botocore.exceptions.ClientError, e:
                self._logger.warning(
                    "Problem tag resource: {0} let's wait a bit".format(str(e)))
                time.sleep(1)

        ig.attach_to_vpc(VpcId=vpc_id)
        return ig

    def load_security_group(self, group_name):
        self._logger.info("Getting security group {0}".format(group_name) )
        filters = [{
            'Name': 'group-name',
            'Values': [group_name]
        }]
        response = self.client.describe_security_groups( Filters=filters)
        security_group_id = response["SecurityGroups"][0]["GroupId"]
        return self.ec2.SecurityGroup(security_group_id)



    def create_security_group(self, build_id, vpc_id, group_name):
        desc = "Security Group {0} for VPC {1}".format(group_name, vpc_id)
        self._logger.info("Creating {0}".format(desc))
        try:
            sg = self.ec2.SecurityGroup(self.client.create_security_group(
                GroupName=group_name,
                Description=desc,
                VpcId=vpc_id
            )['GroupId'])
            sg.authorize_ingress(IpProtocol='tcp', FromPort=0, ToPort=65535, CidrIp='0.0.0.0/0')
            sg.authorize_ingress(IpProtocol='udp', FromPort=0, ToPort=65535, CidrIp='0.0.0.0/0')

            self.add_tags_resource(sg, build_id,[{'Key': 'VpcId', 'Value': vpc_id}], False)
            return sg
        except Exception, e:
            self._logger.error("Could not create security group due to exceptio : ",e )
            return self.load_security_group()



    def create_vpc(self, build_id, dryrun=False):
        self._logger.info("Start to create VPC for %s with cidr_block %s "
        % (build_id, self.cidr_block))
        vpc = self.ec2.Vpc(self.client.create_vpc(CidrBlock=self.cidr_block, DryRun=dryrun)['Vpc']['VpcId'])

        self.add_tags_resource(vpc, build_id)
        ig = self.create_internet_gateway(build_id, vpc.vpc_id)
        self.sg = self.create_security_group(build_id, vpc.vpc_id, self.training_run)
        self.vpc = vpc

        return vpc

    def get_availability_zone(self):
        response = self.client.describe_availability_zones()
        self._logger.info("Got the following AZ: {AvailabilityZones} ".format(**response))
        for d in response["AvailabilityZones"]:
            if d['State'] == "available":
                self._logger.info("Returning {}".format(d))
                return d
        self._logger.error("No AvailabilityZone available!")
        return None


    def create_subnet(self, build_id, vpc_id, subnet_cidrblock, team_id):
        az = self.get_availability_zone()
        if not az:
            raise Exception("Cannot get AvailabilityZone")

        subnet = self.ec2.create_subnet(
            VpcId=vpc_id,
            CidrBlock=subnet_cidrblock,
            AvailabilityZone=az['ZoneName'])


        self.add_tags_resource(subnet, build_id, [{'Key': 'TeamId', 'Value': team_id}])
        return subnet

    def save_keypair_file(self, filename, keypair_material):
        self._logger.info('Storing Key Pair in {0}'.format(os.path.abspath(filename)))
        kfile = open(filename, "w")
        kfile.write("".join(keypair_material))
        kfile.close()


    def create_keypair(self, name=None):
        self._logger.info('Creating new Key Pair for {0}'.format(self.training_run))
        name = self.training_run if name is None else name
        key = self.ec2.create_key_pair(KeyName=name)
        filename = os.path.join(self._basedir, key.key_name + ".pem" )
        self.save_keypair_file( filename, key.key_material  )
        return key

    def launch_team_instance(self, team_id, image_id, subnet_id, private_ip):
        self._logger.info('Launching team {0} instances'.format(team_id))

        response = self.client.run_instances(
            ImageId=image_id,
            MinCount=1,
            MaxCount=1,
            KeyName=self.training_run,
            InstanceType=self.instance_type,
            SubnetId=subnet_id,
            PrivateIpAddress=private_ip,
            InstanceInitiatedShutdownBehavior="terminate")

        instance = self.ec2.Instance(response["Instances"][0]["InstanceId"])

        self.add_tags_resource( instance, "", [{'Key': 'TeamId', 'Value': team_id}], False)

        return instance


    def build_team(self, build_id, vpc, team_id):
        self._logger.info('Creating {0} team'.format(team_id))
        subnet_cidrblock = self._subnet_cidrblocks.pop(0)
        subnet = self.create_subnet(build_id, vpc.vpc_id, subnet_cidrblock, team_id)
        team = Team(team_id, subnet_cidrblock)
        kp = self.create_keypair()
        self.save_keypair_file(self.training_run, kp.key_material)
        instances = []
        for i, ip in enumerate(team.generate_ip()):
            if i < 4:
                continue
            if i > self.number_of_instances+4:
                break
            instances.append(
                self.launch_team_instance(team_id, self.image_id, subnet.subnet_id, ip))


    def build(self, build_id, dryrun=True):
        if dryrun: self._logger.info("Running in dryrun mode ")

        vpc = self.create_vpc(build_id, dryrun)

        for i in xrange(self.number_of_teams):

            team_id = "{0}-{1}".format(self.training_run, i)

            self.build_team(build_id,vpc,team_id)


            #step 3 - create elastic ip

            #step 4 - create keypair

            #step 5 - create instances

            #step 6 - create load balancer

    def destroy(self, build_id):
        pass
