#!/usr/bin/python
import requests
from requests.auth import HTTPDigestAuth
import logging
import argparse
import urlparse
import simplejson as json
import pymongo


class Validator(object):

    def __init__(self, user, apikey, uri, groupid, nodeip):
        self.user = user
        self.apikey = apikey
        self.server = server
        self.groupid = groupid
        self.auth = HTTPDigestAuth(self.user, self.apikey)
        self.session = requests.Session()
        self.nodeip = nodeip

    def validate_replica_members(self):
        mongodburi = "mongodb://{0}/?replicaSet=META"
        mc = pymongo.MongoClient(mongodburi)
        expected_nodes = 3
        assert len(mc.nodes) == expected_nodes,
            "Cannot find the expected number of nodes ({0})".format(expected_nodes)
        assert len(mc.arbiters) == 1, "Expecting to find one arbiter"
        pass

    def validate_replicaset(self, replicaset_name):
        uri = urlparse.urljoin(self.server, "/api/public/v1.0/groups", self.groupid, "/automationConfig")
        r0 = self.session.get(uri, auth=self.auth)

        assert r0.status_code == 200, "Could not retrieve {0} ".format(uri)

        replicasets = r0.json()['replicaSets']

        assert len(replicasets) > 0, "Could not find replica sets :("

        for r in replicasets:
            if r['_id'] == replicaset_name:
                return validate_replica_members()
        assert False, "No luck finding our `{0}` replica set ".format(replicaset_name)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Validate: Replica Set Reconfig')
    parser.add_argument('--server', dest='server', required=True,
    help='ops manager host', type=str)
    parser.add_argument('--user', dest='user', required=True,
    help='ops manager user', type=str)
    parser.add_argument('--apikey', dest='apikey', required=True,
    help='ops manager apikey', type=str)
    parser.add_argument('--groupid', dest='groupid', required=True,
    help='lab group id', type=str)
    parser.add_argument('--nodeip', dest='nodeip', required=True,
    help='ip address of one replica set member', type=str)
    args = parser.parse_args()
    return args

def main():

    args = parse_arguments()
    s = Validator()

    s.build()

if __name__ == '__main__':
    main()
