import unittest
import boto3
import os
from provisioner import Provisioner, Team
from datetime import date, timedelta
from mock import MagicMock
import boto3
from iptools import IpRange
class TestProvisioner(unittest.TestCase):

    def setUp(self):
        self.pr = Provisioner("test1", "default", teams=1)
        self.vpcs = []
        self.subnets = []
        self.keypairfilename = "kkeeyyyy"
        self.keypairs = []

    def tearDown(self):
        self.__destroy()
        self.pr = None
        if os.path.isfile(self.keypairfilename):
            os.remove(self.keypairfilename)


    def __destroy_vpcs(self, vpcs):
        for vpc_id in self.vpcs:
            vpc = self.pr.ec2.Vpc(vpc_id)

            for ig in vpc.internet_gateways.all():
                vpc.detach_internet_gateway(InternetGatewayId=ig.id)
                self.__destructor.delete_internet_gateway(InternetGatewayId=ig.id)
            print self.__destructor.delete_vpc(VpcId=vpc_id)

    def __destroy_subnets(self, subnets):
        for subnet_id in self.subnets:
            print self.__destructor.delete_subnet(SubnetId=subnet_id)

    def __destroy_keypairs(self, keypairs):
        print "Destroy KeyPairs"

        for keypair in self.keypairs:
            try:
                print self.__destructor.delete_key_pair(KeyName=keypair)
            except Exception, e:
                print e


    def __destroy(self):
        try:
            self.__destructor = self.pr.client
            print "Destroy subnets"
            self.__destroy_subnets(self.subnets)
            print "Destroy Objects VPCS"
            self.__destroy_vpcs(self.vpcs)
            self.__destroy_keypairs(self.keypairs)

        except Exception, e:
            print 'Problem destorying objects {0}'.format(str(e))

    def __base_pr_vpc(self):
        self.pr.connect()
        vpc = self.pr.create_vpc("build_id")
        self.vpcs.append(vpc.vpc_id)

        return vpc


    def __test_incorrect_date(self, end_date):
        with self.assertRaises(Exception) as cmd:
            Provisioner("test1", "default", end_date=end_date)

        the_exception = cmd.exception

        expected_exception_msg = "end_date %s cannot be before today or set for more than 30 days: %s " % (end_date, date.today())
        self.assertEquals( str(the_exception), expected_exception_msg)

    def test_prior_than_today_enddate(self):
        end_date = date.today() - timedelta(days=1)
        self.__test_incorrect_date(end_date)

    def test_end_date_today(self):
        end_date = date.today()
        prov = Provisioner("test1", "default", end_date=end_date)

        self.assertEquals( prov.end_date, end_date)

    def test_end_date_in_31_days(self):
        end_date = date.today() + timedelta(days=31)
        self.__test_incorrect_date(end_date)

    def test_numberofteams_gt10(self):
        with self.assertRaises(Exception) as cmd:
            Provisioner("test1", "default", end_date=end_date, teams=11)

    def test_numberofteams_lt1(self):
        with self.assertRaises(Exception) as cmd:
            Provisioner("test1", "default", end_date=end_date, teams=0)

    def test_empty_training_run(self):
        with self.assertRaises(Exception) as cmd:
            Provisioner("")
        the_exception = cmd.exception

        self.assertEquals("training_run cannot be empty", str(the_exception))

    def test_None_training_run(self):
        with self.assertRaises(Exception) as cmd:
            Provisioner(training_run=None)
        the_exception = cmd.exception

        self.assertEquals("training_run cannot be empty", str(the_exception))

    def test_connection_get_session(self):
        pr = Provisioner("test1", "default", teams=1)
        pr.connect()
        self.assertIsNotNone(pr.session)

    def test_ec2_no_connect(self):
        pr = Provisioner("test1", "default", teams=1)
        with self.assertRaises(Exception) as cmd:
            pr.ec2

        the_exception = cmd.exception
        expected_exception_msg = "EC2 resource cannot be empty. Don't forget to connect()!"
        assert str(the_exception) == expected_exception_msg

    def test_session_no_connect(self):
        pr = Provisioner("test1", "default", teams=1)
        with self.assertRaises(Exception) as cmd:
            pr.session

        the_exception = cmd.exception
        expected_exception_msg = "Session cannot be None"
        assert str(the_exception) == expected_exception_msg

    def test_cidr_block(self):
        self.pr.cidr_block = '27.0.17.0/24'
        from iptools.ipv4 import validate_cidr
        assert True == validate_cidr('27.0.17.0/24')

    def test_incorrect_cidr_block(self):

        with self.assertRaises(Exception) as cmd:
            cidr = "09.3423.34234234.32/30"
            self.pr.cidr_block = cidr

        the_exception = cmd.exception
        expected_exception_msg = 'Incorrect CIDR BLOCK %s' % (cidr)
        self.assertEquals(str(the_exception), expected_exception_msg)


    def test_client_ok(self):
        self.pr.connect()
        assert self.pr.client != None

    def test_create_vpc(self):
        dryrun = False
        self.pr.connect()
        vpc = self.pr.create_vpc("build_id", dryrun)
        self.vpcs.append(vpc.vpc_id)

        assert vpc != None

    def test_add_tag_to_vpc(self):
        vpc = self.__base_pr_vpc()
        assert any(d['Key'] == 'Owner' and d['Value'] == 'Advanced Training' for d in vpc.tags)

    def test_get_availability_zones(self):
        vpc = self.__base_pr_vpc()
        assert self.pr.get_availability_zone() != None


    def test_create_subnet(self):
        vpc = self.__base_pr_vpc()
        subnet_cidr_bloc = "27.0.17.0/27"
        team_id = "aaaa"

        subnet = self.pr.create_subnet("build_id", vpc.vpc_id, subnet_cidr_bloc, team_id)
        self.subnets.append(subnet.subnet_id)
        assert subnet != None

    def test_create_security_group(self):
        vpc = self.__base_pr_vpc()

        description = "{0} run security group".format(self.pr.training_run)

        group_name = self.pr.training_run

        sg = self.pr.create_security_group(vpc_id, group_name, description)

        response = self.pr.client.describe_security_group()

        assert response != None

        assert not sg.name

    def test_save_keypair_file(self):

        self.pr.save_keypair_file(self.keypairfilename, "YO BRO")

        assert os.path.isfile(self.keypairfilename)

        material = open(self.keypairfilename, "r").readlines()

        assert material == ["YO BRO"]


    def test_create_keypair(self):
        self.pr.connect()

        filename = "test1.pem"

        key = self.pr.create_keypair()

        self.keypairs.append(key.key_name)

        assert os.path.isfile(filename)

        self.assertEqual( key.key_material , "".join(open(filename, "r").readlines()))

    def test_get_security_group(self):
        self.pr.connect()

        security_group_name = "tst"
        sg = self.pr.load_security_group(security_group_name)
        assert sg
        assert sg.group_name == security_group_name


class TestTeam(unittest.TestCase):

    def tearDown(self):
        pass

    def setUp(self):
        self.cidr_block = "27.0.17.64/27"
        self.team = Team("superteam", self.cidr_block)

    def test_init(self):
        with self.assertRaises(Exception) as cmd:
            team = Team("", 111)

        the_exception = cmd.exception
        assert 'team_id cannot be empty' == str(the_exception)

    def test_next_ip(self):
        r = IpRange(self.cidr_block)
        for i,ip in enumerate(self.team.generate_ip(), start=1):
            assert ip in r
            if i > 15: return

    def test_apppend_None_instance(self):
        with self.assertRaises(Exception) as cmd :
            self.team.append_instance(None)
        assert "Cannot append empty instance" == str(cmd.exception)

    def test_apppend_Empty_instance(self):
        with self.assertRaises(Exception) as cmd :
            self.team.append_instance("")
        assert "Cannot append empty instance" == str(cmd.exception)


if __name__ == "__main__":
    unittest.main()
