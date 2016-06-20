import boto3
from botocore.exceptions import *
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

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

class Team(object):
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logging.basicConfig(format=FORMAT)
    log.setLevel(logging.DEBUG)
    log = logging.getLogger(__name__)

    def __init__(self, team_id, subnet_id, cidr_block):
        """
        Class that manages created teams
        """
        self.team_id = team_id
        self.cidr_block = cidr_block
        self._instances = []
        self._public_instance = {}
        self._n_opsmgr = 2
        self._opsmgr_instances = []
        self.subnet_id = subnet_id

    @property
    def opsmgr_instances(self):
        return self._opsmgr_instances

    @property
    def load_balancer(self):
        return self._load_balancer

    @load_balancer.setter
    def load_balancer(self, lb):
        self._load_balancer=lb

    @property
    def subnet_id(self):
        return self._subnet_id

    @subnet_id.setter
    def subnet_id(self, subnet):
        self._subnet_id = subnet


    @property
    def public_instance(self):
        if self._public_instance:
            return self._public_instance
        raise Exception("No Public Instance Set Yet!")

    @public_instance.setter
    def public_instance(self, instance):
        if isinstance(instance, dict):
            if instance.has_key("allocation_id") and instance.has_key("instance_id") and instance.has_key("public_ip"):
                self._public_instance = instance
            else:
                raise Exception("{0} does not contain `allocation_id` or `instance_id` or `public_ip`".format(instance))
        else:
            raise Exception("public instance has to be `dict`")

    @property
    def instances(self):
        return self._instances

    def add_instance(self, instance):
        if self._instances:
            self._instances = []
        if len(self._opsmgr_instances) < self._n_opsmgr:
            self._opsmgr_instances.append(instance)
        self._instances.append(instance)

    def __repr__(self):
        return """
        TEAMID - {0}
        INSTANCES - {1}
        KEYPAIR_FILEPATH - {2}
        """.format(self.team_id, self._instances)

    @property
    def keypair_file(self):
        return self._keypair_file

    @keypair_file.setter
    def keypair_file(self, filepath):
        if not os.path.isfile(filepath):
            raise Exception("Cannot set non-file path as keypair file: {0}".format(filepath))
        self._keypair_file

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

    @property
    def load_balancer_name(self):
        return self.team_id + "-lb"

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
        self.cidr_block = '27.0.17.0/24'
        self._subnet_cidrblocks = [
            "27.0.17.0/27",
            "27.0.17.32/27",
            "27.0.17.64/27",
            "27.0.17.96/27",
            "27.0.17.128/27"]
        self.teams = []
        self._basedir = "."
        self.number_of_instances = 1
        self.instance_type = 'm3.xlarge'
        self.image_id = "ami-d63cccbb"

    @property
    def basedir(self):
        return self._basedir

    @basedir.setter
    def basedir(self, dirpath):
        if not os.path.isdir(dirpath):
            raise Exception('Cannot set {0} as base dir. Not dir'.format(dirpath))
        self._basedir = dirpath


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

    def add_team(self, team):
        self.teams.append(team)

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
        log.debug("get training_run: %s", self._training_run)
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
        log.debug("get end_date: %s", self.training_run)
        return self._edate

    @end_date.setter
    def end_date(self, d):
        if  date.today() > d or d > date.today()+timedelta(days=30) : raise Exception("end_date %s cannot be before today or set for more than 30 days: %s " % (d, date.today()))
        self._edate = d

    @property
    def session(self):
        if not self._session: raise Exception("Session cannot be None")
        log.debug("get session: %s", self.training_run)
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
        self.elb = self.session.client('elb')

    def get_default_tags(self):
        return [
            {'Key': 'BUILDID', 'Value': self.training_run},
            {'Key': 'Name', 'Value': self.training_run},
            {'Key': 'Owner', 'Value': 'Advanced Training'},
            {'Key': 'Expire', 'Value': self.end_date.strftime("%s")}
            ]


    def add_tags_resource(self, resource, name, tags=[], statefull=True):
        """
        Adds all required tags for AWS account management:
        - Name: training_run
        - expires: end_date
        - Owner: "Advanced Training"

        """
        tags += self.get_default_tags()
        log.info(
        "Adding tags %s to resource %s " % (str(tags), resource.id ))

        if statefull:
            c = 5
            while resource.state not in ["available", "running"] :
                log.info(
                    "Resource {0} not yet available - current state {1}".format(resource.id, resource.state))
                time.sleep(1)
                c=-1
                if c < 1:
                    break
                resource.reload()
        resource.create_tags(Tags=tags)

    def create_internet_gateway(self, build_id, vpc_id):
        log.info(
        "Creating Internet Gateway for {0} on vpc {1}".format(build_id, vpc_id))
        response = self.client.create_internet_gateway()

        ig = self.ec2.InternetGateway(response['InternetGateway']['InternetGatewayId'])

        retries = 2
        tags = [{'Key': 'VpcId', 'Value': vpc_id}]
        while retries > 0 :
            try:
                retries-=1
                self.add_tags_resource(ig, build_id, tags, False)
            except ClientError, e:
                log.warning("Problem tag resource: {0} let's wait a bit".format(str(e)))
                time.sleep(1)

        ig.attach_to_vpc(VpcId=vpc_id)
        self.ig = ig
        return ig

    def load_security_group(self, group_name):
        log.info("Getting security group {0}".format(group_name) )
        filters = [{
            'Name': 'group-name',
            'Values': [group_name]
        }]
        response = self.client.describe_security_groups( Filters=filters)
        security_group_id = response["SecurityGroups"][0]["GroupId"]
        return self.ec2.SecurityGroup(security_group_id)


    def define_vpc_routes(self, ig):
        log.debug("Adding route to {0}".format(ig))
        try:
            for rt in self.vpc.route_tables.all():
                rt.create_route(
                    DestinationCidrBlock="0.0.0.0/0",
                    GatewayId=ig.id
                )
        except Exception, e:
            log.error("Could not define_vpc_routes: {0}".format(e))
            log.error("Need to proceed w/ manual definition for ig {0} and subnet {1}".format(ig, subnet))


    def create_security_group(self, build_id, vpc_id, group_name):
        desc = "Security Group {0} for VPC {1}".format(group_name, vpc_id)
        log.info("Creating {0}".format(desc))
        resp = self.client.create_security_group(
            GroupName=group_name,
            Description=desc,
            VpcId=vpc_id
        )
        log.info("Got response {0}".format(resp))

        if not resp.has_key('GroupId'):
            log.error('Cannot create new security group.', resp)
            return self.load_security_group(group_name)
        sgid = resp['GroupId']
        try:
            sg = self.ec2.SecurityGroup(sgid)
            sg.authorize_ingress(IpProtocol='tcp', FromPort=0, ToPort=65535, CidrIp='0.0.0.0/0')
            sg.authorize_ingress(IpProtocol='udp', FromPort=0, ToPort=65535, CidrIp='0.0.0.0/0')

            self.add_tags_resource(sg, build_id,[{'Key': 'VpcId', 'Value': vpc_id}], False)
            return sg
        except Exception, e:
            log.error("Could not create security group due to exception : {0} ".format(e) )
            return self.load_security_group(group_name)


    def create_vpc(self, build_id, dryrun=False):
        log.info("Start to create VPC for {0} with cidr_block {1} ".format(build_id, self.cidr_block))
        vpc = self.ec2.Vpc(self.client.create_vpc(CidrBlock=self.cidr_block, DryRun=dryrun)['Vpc']['VpcId'])
        retries = 3
        while retries > 0:
            retries=-1
            try:
                log.debug("Current VPC state: {}".format(vpc.state))
                self.add_tags_resource(vpc, build_id)
            except Exception, e:
                log.error("Could not create VPC {}".format(vpc))

        self.sg = self.create_security_group(build_id, vpc.vpc_id, self.training_run)
        self.vpc = vpc
        ig = self.create_internet_gateway(build_id, vpc.vpc_id)
        self.define_vpc_routes(ig)
        return vpc

    def get_availability_zone(self):
        response = self.client.describe_availability_zones()
        log.info("Got the following AZ: {AvailabilityZones} ".format(**response))
        for d in response["AvailabilityZones"]:
            if d['State'] == "available":
                log.info("Returning {}".format(d))
                return d
        log.error("No AvailabilityZone available!")
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
        log.info('Storing Key Pair in {0}'.format(os.path.abspath(filename)))
        with open(filename, "w") as kfile:
            kfile.write("".join(keypair_material))
        os.chmod(filename, 0400)


    def create_keypair(self, name=None):
        log.info('Creating new Key Pair for {0}'.format(self.training_run))
        name = self.training_run if name is None else name
        filename = os.path.join(self._basedir, name + ".pem" )
        try:
            key = self.ec2.create_key_pair(KeyName=name)
            self.save_keypair_file( filename, key.key_material  )
            return key
        except Exception, e:
            log.error("could not create keypair: {0}".format(e))
            import binascii
            new_name = binascii.hexlify(os.urandom(10))
            log.warning( "creating new random {0} key".format(filename))
            return self.create_keypair(new_name)



    def launch_team_instance(self, team_id, image_id, subnet_id, private_ip):
        log.info('Launching team {0} instances'.format(team_id))

        response = self.client.run_instances(
            ImageId=image_id,
            MinCount=1,
            MaxCount=1,
            KeyName=self.training_run,
            InstanceType=self.instance_type,
            SubnetId=subnet_id,
            PrivateIpAddress=private_ip,
            SecurityGroupIds=[self.sg.id],
            InstanceInitiatedShutdownBehavior="terminate")
        instance_id = response["Instances"][0]["InstanceId"]
        instance = self.ec2.Instance(instance_id)
        try:
            self.add_tags_resource( instance, "", [{'Key': 'TeamId', 'Value': team_id}], True)
        except Exception, e:
            log.warning("Could not add tags to instance {0} - need to check manually".format(instance_id) )

        return instance


    def allocate_elastic_ip_instance(self,allocation_id, instance):
        #retries = 5
        while not instance.state['Name'] == 'running':
            log.debug("Not there yet. Current state - {0} sleep a bit".format(instance.state))
            time.sleep(2)
            instance.reload()
            #retries=-1

        resp = self.client.associate_address(
            InstanceId=instance.id,
            AllocationId=allocation_id)

        log.debug("Allocated elastic ip {0} to {1} instance".format(allocation_id,instance.id))


    def allocate_elastic_ip(self, team):
        try:
            instance = team.instances[-1]
            resp = self.client.allocate_address(Domain='vpc')
            self.allocate_elastic_ip_instance(resp['AllocationId'],instance)
            team.public_instance = {
                'allocation_id': resp['AllocationId'],
                'public_ip': resp['PublicIp'],
                'instance_id': instance.id,
                }

            log.debug("public_instance {0}".format(team.public_instance))

        except Exception, e:
            log.error('Could not allocate elastic ip due to exception: {0}'.format(e))

    def create_loadblancer(self, team):
        log.debug("Creating Load Balancer for {0}".format(team.team_id))
        try:
            team.load_balancer = self.elb.create_load_balancer(
                LoadBalancerName=team.load_balancer_name,
                Listeners=[
                    {
                    'Protocol': 'HTTP',
                    'LoadBalancerPort': 80,
                    'InstanceProtocol': 'HTTP',
                    'InstancePort': 8080,
                    }],
                Subnets=[team.subnet_id],
                SecurityGroups=[self.sg.id],
                Tags=self.get_default_tags(),
            )

            log.debug("Load Balancer {0} created".format(team.load_balancer_name))

        except Exception, e:
            log.error("Could not create load balancer: {0}".format(e))

    def register_instances(self, team):
        try:
            instance_ids = []
            for n in team.opsmgr_instances:
                instance_ids.append({"InstanceId": n.id})
            resp = self.elb.register_instances_with_load_balancer(
                LoadBalancerName=team.load_balancer_name,
                Instances=instance_ids
            )

            log.debug( "registered {0} instances with load balancer {1}".format(
                instance_ids, team.load_balancer_name))
        except Exception, e:
            log.error("Could not register instances with load balancer {0} due to {1}".format(team.load_balancer_name, e))

    def build_team(self, build_id, vpc, team_id):
        log.info('Creating {0} team'.format(team_id))
        subnet_cidrblock = self._subnet_cidrblocks.pop(0)
        subnet = self.create_subnet(build_id, vpc.vpc_id, subnet_cidrblock, team_id, )

        team = Team(team_id, subnet.id, subnet_cidrblock)
        kp = self.create_keypair()
        instances = []
        for i, ip in enumerate(team.generate_ip()):
            if i < 4:
                continue
            if i > self.number_of_instances+4:
                break
            team.add_instance(self.launch_team_instance(team_id, self.image_id,
                subnet.subnet_id, ip))

        self.allocate_elastic_ip(team)

        self.create_loadblancer(team)
        self.register_instances(team)

        self.add_team(team)

    def build(self, build_id, dryrun=True):
        if dryrun: log.info("Running in dryrun mode ")

        vpc = self.create_vpc(build_id, dryrun)
        teams = []
        for i in xrange(self.number_of_teams):

            team_id = "{0}-{1}".format(self.training_run, i)

            self.build_team(build_id,vpc,team_id)

            #step 6 - create load balancer

    def destroy_load_balancer(self, load_balancer_name, instance_ids):
        try:
            log.info(self.elb.deregister_instances_from_load_balancer(
                LoadBalancerName=load_balancer_name,
                Instances=[ {"InstanceId": x} for x in instance_ids]))

            log.info(self.elb.delete_loadbalancer(LoadBalancerName=load_balancer_name))
        except Exception, e:
            log.error("could not delete load balancer {0}: {1}".format(load_balancer_name, e))

    def destroy(self):
        filters = [{
            'Name': 'tag:BUILDID',
            'Values': [self.training_run]
        }]
        #terminate instances
        for i in self.ec2.instances.filter(Filters=filters):
            log.debug("Terminating {0} instance".format(i))
            i.terminate()

        for vpc in self.ec2.vpcs.filter(Filters=filters):
            destroy_vpc(vpc)


def delete_dependency(dep):
    try:
        log.info("Deleting {0} ".format(dep))
        dep.delete()
    except Exception, e:
        log.warning("Could not delete {0} due to {1}".format(dep, e))

def destroy_vpc(vpc):
    filters = [{
        'Name': 'tag:VpcId',
        'Values': [vpc.id]
    }]
    log.debug("Deleting vpc {0} ".format(vpc))

    #instances
    for i in vpc.instances.all():
        while i.state['Name'] != "terminated":
            log.info("Instance {0} not yet terminated {1}. We will try again in a short while".format(i, i.state))
            i.terminate()
            i.reload()

            time.sleep(2)
    try:
    #internet gateways
        for ig in vpc.internet_gateways.all():
            vpc.detach_internet_gateway(InternetGatewayId=ig.id)
            delete_dependency(ig)

        #subnets
        for sn in vpc.subnets.all():
            delete_dependency(sn)
        #and routing tables
        for rt in vpc.route_tables.all():
            delete_dependency(rt)
        #security groups
        for sg in vpc.security_groups.filter(Filters=filters):
            delete_dependency(sg)
        #Networl ACLS
        for nac in vpc.network_acls.all():
            delete_dependency(nac)

        #Networl Interfaces
        for ni in vpc.network_interfaces.all():
            delete_dependency(ni)

        #requested_vpc_peering_connections
        for n in vpc.requested_vpc_peering_connections.all():
            delete_dependency(n)


        vpc.delete()

    except Exception, e:
        log.error('Could not delete VPC {0} due to {0}'.format(vpc.id, e))
