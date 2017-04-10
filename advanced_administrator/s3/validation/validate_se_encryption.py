#!/usr/bin/python

# Validate that a storage engine is running encryption

# TODOs
#  - support cmd line options, instead of just config files

import argparse
import commands
import logging
import os
import os.path
import re

Default_Config_File = '/etc/mongod.cnf'

log = logging.getLogger(__name__)
log.setLevel('DEBUG')
handler = logging.StreamHandler()
f = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(f)
handler.setLevel('DEBUG')
log.addHandler(handler)

def get_string(regex, string):
    m = re.search(regex, string)
    if m:
        found = m.group(1)
    else:
        raise Exception("Can't extract regex {} in string {}".format(regex, string))
    return found

class Validator(object):

    def __init__(self, configfile, verbose):
        self.configfile = configfile
        self.verbose = verbose

    def validate_encryption(self):
        # Get the DB path from the config file
        if not os.path.exists(self.configfile):
            assert False, "Cannot find config file {0}".format(self.configfile)

        with open(self.configfile) as f:
            file_contents = f.read()
        dbpath = get_string("\sdbPath\s*:\s*['\"]?(.+?)['\"]?\s", file_contents)
        assert dbpath, "Can't identify DB path"

        # Look for non-encrypted data in the DB files
        # TODO - handle DB per directory
        # TODO - ensure there are collections under that path
        cmd = "/usr/bin/grep _id collection* 2>&1"
        if self.verbose:
            print("Running cmd: {}".format(cmd))
            print("in dir: {}".format(dbpath))
        os.chdir(dbpath)
        (ret, out) = commands.getstatusoutput(cmd)
        if self.verbose:
            print("RET: {}".format(ret))
            print("OUT: {}".format(out))

        if len(out) > 0:
            assert False, "Found non-encrypted data under {0}".format(dbpath)

        if ret != 256:
            assert False, "Could not check for collections under {0}".format(dbpath)

        return True

    def get_configfile(self):
        if self.configfile is None:
            (ret, out) = commands.getstatusoutput("ps -eaf | grep mongod")
            m = re.match("^.*(-f|--config)\s+(\S+).*", out)
            if m:
                self.configfile = m.group(2)
                if self.verbose:
                    print("Config file from the cmd line is: {}".format(self.configfile))
            else:
                raise Exception("Can't extract config file name for mongod process")
        return


def parse_arguments():
    parser = argparse.ArgumentParser(description='Verify Lab: Database is encrypted')
    parser.add_argument('--configfile', dest='configfile',
        help='ops manager host', type=str)
    parser.add_argument('--verbose', dest='verbose', action='store_true',
        help='display more info')

    args = parser.parse_args()
    return args

def main():

    args = parse_arguments()

    v = Validator(args.configfile, args.verbose)
    v.get_configfile()
    res = v.validate_encryption()

    assert res, "not all tests passed!"

    log.debug("OK, All Good")

if __name__ == '__main__':
    main()
