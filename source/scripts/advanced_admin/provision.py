import boto3
from botocore.exceptions import ClientError
import logging


SECURITY_GROUP_NAME = 'Advanced Administrator'
log = logging.getLogger('provision')
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())



def check_security_group_exists(client, security_group_name):
    """
    Checks if a given security group exists in the client region
    """
    #currently we are using a fixed Security Group tag Name "Advanced Administrator", possible improment in the futre
    groupnames = [security_group_name]
    sgs = client.describe_security_groups(GroupNames=groupnames)['SecurityGroups']
    if len(sgs) > 0:
        return sgs[0]['GroupId']

    return None

def set_security_group_rules(resource, sg):
    """
    Adds the required security group ingress authorization rules to th
    """



def create_security_group(client, resource, security_group_name):
    sg = None
    try:
        response = client.create_security_group(
            GroupName=security_group_name,
            Description="Security Group fro Advanded Administror Training"
        )

        log.debug('create_security_group: ' + str(response))

        sg = resource.SecurityGroup(response['GroupId'])
    except ClientError, e:
        log.error( e )
        log.debug("security group already exists so we are recovering the group")
        sg = resource.SecurityGroup( check_security_group_exists(client, security_group_name))

    import ipdb;ipdb.set_trace()
    return sg


session = boto3.Session(profile_name='default')

ec2 = session.resource('ec2')
client = session.client('ec2')


sg = create_security_group(client, ec2, SECURITY_GROUP_NAME)
