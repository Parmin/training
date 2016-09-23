#!/usr/bin/python
import argparse
import urlparse
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
import simplejson as json
import re
import logging

log = logging.getLogger(__name__)
log.setLevel('DEBUG')
handler = logging.StreamHandler()
f = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(f)
handler.setLevel('DEBUG')
log.addHandler(handler)

class Validator(object):

    def __init__(self, server, user, apikey):

        self.server = server
        self.user = user
        self.apikey = apikey
        self.session = requests.Session()
        self.groupname = "VERYSAFE"
        self.replicasetname = "SECURE"
        self.auth=HTTPDigestAuth(self.user, self.apikey)

    def get_group_self_link(self, group):
        for link in group['links']:
            if link['rel'] == "self":
                return link['href']
        return None

    def validate_secured_replicaset(self):
        uri = urlparse.urljoin(self.server, "/api/public/v1.0/groups")

        r0 = self.session.get(uri, auth=self.auth)

        assert r0.status_code == 200, "Cannot connect to opsmanager API {0}".format(r0.status_code)
        group = self.validate_group_name(r0.json())

        assert group != None,  "Could not find group name {0}".format(self.groupname)
        assert group['publicApiEnabled'], "API not enabled"

        link = self.get_group_self_link(group)

        r1 = self.session.get(link, auth=self.auth)
        return True

    def validate_group_name(self, json):
        for d in json['results']:
            if d['name'] == self.groupname:
                return d

        return None

    def get_replicaset(self, link, clustername):
        r2 = self.session.get(link, auth=self.auth)
        assert r2.status_code == 200, "Problem fetching group clusters"

        for cluster in r2.json()['results']:
            if cluster['replicaSetName'] == clustername:
                for link in cluster['links']:
                    if link['rel'] == "self":
                        r3 = self.session.get(link['href'], auth=self.auth)
                        assert r3.status_code == 200, "Problem fetching group clusters"
                        return r3.json()
        return None


    def validate_replicaset_created(self, group):
        for link in group['links']:
            if link['rel'] == "http://mms.mongodb.com/clusters":
                replica = self.get_replicaset(link['href'])
                assert replica != None, "ReplicaSet not found!"


def parse_arguments():
    parser = argparse.ArgumentParser(description='Verify Lab: Secured Replica Set')
    parser.add_argument('--server', dest='server', required=True,
    help='ops manager server', type=str)
    parser.add_argument('--user', dest='user', required=True,
    help='ops manager user', type=str)
    parser.add_argument('--apikey', dest='apikey', required=True,
    help='ops manager apikey', type=str)

    args = parser.parse_args()
    return args

def main():

    args = parse_arguments()

    v = Validator(args.server, args.user, args.apikey)

    assert v.validate_secured_replicaset(), "not all tests passed!"

    log.debug("OK, All Good")

if __name__ == '__main__':
    main()
