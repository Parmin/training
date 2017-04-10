#!/usr/bin/python

# Validate that log redaction has been enabled for a given MongoDB node
#  --redactClientLogData

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

    def validate_redaction(self):
        # Get the log path from the config file
        if not os.path.exists(self.configfile):
            assert False, "Cannot find config file {0}".format(self.configfile)

        with open(self.configfile) as f:
            file_contents = f.read()
        logpath = get_string("\spath\s*:\s*['\"]?(.+?)['\"]?\s", file_contents)
        assert logpath, "Can't identify log path"

        # Look for non-redacted data in the log files
        cmd = "/usr/bin/grep '_id: \"[^#]' " + logpath + " 2>&1"
        if self.verbose:
            print("Running cmd: {}".format(cmd))
            print("in dir: {}".format(logpath))
        (ret, out) = commands.getstatusoutput(cmd)
        if self.verbose:
            print("RET: {}".format(ret))
            print("OUT: {}".format(out[0:256]))

        if len(out) > 0:
            assert False, "Found non-redacted log entries in {0}".format(logpath)

        if ret != 256:
            assert False, "Could not check for log file {0}".format(logpath)

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
    parser = argparse.ArgumentParser(description='Verify Lab: Log redaction is enabled')
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
    res = v.validate_redaction()

    assert res, "not all tests passed!"

    log.debug("OK, All Good")

if __name__ == '__main__':
    main()
