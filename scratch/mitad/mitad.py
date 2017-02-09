#!/usr/bin/env python

"""
Construct a catalog of some MongoDB knowledge from different sources.

Usage:
    mitad -h
    mitad [--verbose] [--mongodb=<conn_string>] [--db=<database>] <source> ...

At this point, the sources are:
    - online courses
    - in-person courses
    - docs repository

If processing of the sources succeeds, the script returns 0.
Otherwise, returns non 0 and hopefully appropriate error messages.

Options:
    -h --help               Show this help text.
    --db=<database>         Database in which to store the information [default: mitad]
    --mongodb=<conn_string> Connection string to the instance [default: localhost:27017]
    -v --verbose            Print more information about the processing
    <source> ...            Sources to process. Those must be paths to a file system

Examples:
    python mitad.py --verbose ./training-sw ./university-courses-sw ./docs
"""
# end docopt usage string

# implementation notes
"""
- uses tags of the form
    .. KI <key> : <value>
  in the .txt files that are pre-processed by Giza.
  Those line are discarded by Giza (not .. )

TODOs:
    - add base class for common code
    - count the number of files pre-processed
    - report all errors encountered at the end
    - report some stats at the end
    - support sources as GitHub refs instead of local repos
"""

import glob
import json
import logging
import os
import pymongo
import re
import shutil
import subprocess
import sys

from datetime import datetime
from docopt import docopt

DB_obj = None
Exit_code = 0
Verbose = False                         # May want to allow for many levels of verbosity

# How we store info in the collections
Store_contents_as_array = True
Store_title_in_contents = True

DB_item = 'item'
KI_regex = "^\.\. KI\s+(.+)\s*:(.+)$"   # Matching the KI directives in the files processed by Giza

def identify_source(path):
    cmd = "git remote get-url origin"
    os.chdir(path)
    try:
        type = "Unidentified"
        out = run_cmd(cmd).rstrip()
        if out == "https://github.com/mongodb/docs":
            type = "docs"
        elif out == "https://github.com/10gen/training":
            type = "training"
        elif out == "https://github.com/10gen/university-courses":
            type = "university"
        else:
            raise Exception("Can't identify repository type from path {}".format(path))
        if is_verbose_enough():
            print("  Repo type: {}".format(type))
    except:
        raise Exception("FATAL - Can't identify repository type from path {}".format(path))
    return type

def is_verbose_enough():
    return Verbose

def run_cmd(cmd):
    cmd_list = cmd.split(" ")
    output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
    return output.decode("utf-8")

'''
Base class for all RST based repositories
'''
class Base_rst(object):
    def __init__(self, path):
        self.path = path
        print("Processing source: {}".format(self.path))

    def get_files(self, dirs):
        all_files = []
        for one_dir in dirs:
            path = os.path.join(self.path, one_dir)
            paths = glob.glob(path)
            all_files = all_files + paths
        all_files.sort()
        return all_files


class Docs(Base_rst):
    def __init__(self, path):
        super().__init__(path)

    def parse(self):
        ret = True
        dirs = ['source/*.txt', 'source/*/*.txt', 'source/reference/*/*.txt']
        files = self.get_files(dirs)
        for one_file in files:
            try:
                # Some files (6?) like "training/source/modules/aggregation.txt" have format isssues, so let's skip them
                if is_verbose_enough():
                    print("    File: {}".format(one_file))
                pages = 0
                current_section = ''
                current_page = ''
                page_title = ''
                previous_line = ''
                keywords = []
                with open(one_file) as file_obj:
                    if re.match(".*tutorial.*", one_file):
                        knowledge_type = "tutorial"
                    else:
                        knowledge_type = "docs"
                    for one_line in file_obj:
                        if re.match("^\=+$", one_line):
                            current_section = previous_line.rstrip()
                        if re.match("^\-+$", one_line):
                            # Complete the previous page, however we have one too many line in it
                            len_last_line = len(previous_line)
                            current_page = current_page[:-len_last_line]
                            if page_title != '':
                                if Store_contents_as_array == True:
                                    current_page_to_insert = current_page.split("\n")
                                else:
                                    current_page_to_insert = current_page
                                DB_obj[DB_item].insert({'type': knowledge_type,
                                                        'path': one_file,
                                                        'section': current_section,
                                                        'title': page_title,
                                                        'keywords': keywords,
                                                        'contents': current_page_to_insert})
                            # Let's start our new page
                            if Store_title_in_contents == True:
                                current_page = previous_line
                            pages += 1
                            page_title = previous_line.rstrip()
                            if is_verbose_enough():
                                print("        page title: {}".format(page_title))
                        current_page = current_page + one_line
                        previous_line = one_line
                    if is_verbose_enough():
                        print("      pages: {}".format(pages))
            except:
                print("ERROR - in reading file: {}".format(one_file))
        return ret


class Training(Base_rst):
    def __init__(self, path):
        super().__init__(path)

    def parse(self):
        ret = True
        dirs = ['source/modules/*.txt', 'source/modules/internal/*.txt']
        files = self.get_files(dirs)
        for one_file in files:
            try:
                # Some files (6?) like "training/source/modules/aggregation.txt" have format isssues, so let's skip them
                if is_verbose_enough():
                    print("    File: {}".format(one_file))
                pages = 0
                current_section = ''
                current_page = ''
                page_title = ''
                previous_line = ''
                keywords = []
                with open(one_file) as file_obj:
                    if re.match(".*internal.*", one_file):
                        knowledge_type = "nhtt"
                    else:
                        knowledge_type = "in-person"
                    for one_line in file_obj:
                        if re.match("^\=+$", one_line):
                            current_section = previous_line.rstrip()
                        if re.match("^\-+$", one_line):
                            # Complete the previous page, however we have one too many line in it
                            len_last_line = len(previous_line)
                            current_page = current_page[:-len_last_line]
                            if page_title != '':
                                if Store_contents_as_array == True:
                                    current_page_to_insert = current_page.split("\n")
                                else:
                                    current_page_to_insert = current_page
                                DB_obj[DB_item].insert({'type': knowledge_type,
                                                        'path': one_file,
                                                        'section': current_section,
                                                        'title': page_title,
                                                        'keywords': keywords,
                                                        'contents': current_page_to_insert})
                            # Let's start our new page
                            if Store_title_in_contents == True:
                                current_page = previous_line
                            pages += 1
                            page_title = previous_line.rstrip()
                            if is_verbose_enough():
                                print("        page title: {}".format(page_title))
                        current_page = current_page + one_line
                        previous_line = one_line
                    if is_verbose_enough():
                        print("      pages: {}".format(pages))
            except:
                print("ERROR - in reading file: {}".format(one_file))
        return ret


class University(Base_rst):
    def __init__(self, path):
        super().__init__(path)

    def parse(self):
        ret = True
        dirs = ['src/lessons/*.rst', 'src/lessons/*/*.rst']
        files = self.get_files(dirs)
        for one_file in files:
            try:
                if is_verbose_enough():
                    print("    File: {}".format(one_file))
                pages = 0
                current_section = ''
                current_page = ''
                page_title = ''
                previous_line = ''
                keywords = []
                with open(one_file) as file_obj:
                    for one_line in file_obj:
                        if re.match("^\=+$", one_line):
                            current_section = previous_line.rstrip()
                        if re.match("^\-+$", one_line):
                            # Complete the previous page, however we have one too many line in it
                            len_last_line = len(previous_line)
                            current_page = current_page[:-len_last_line]
                            if page_title != '':
                                if Store_contents_as_array == True:
                                    current_page_to_insert = current_page.split("\n")
                                else:
                                    current_page_to_insert = current_page
                                DB_obj[DB_item].insert({'type': 'online',
                                                        'path': one_file,
                                                        'section': current_section,
                                                        'title': page_title,
                                                        'keywords': keywords,
                                                        'contents': current_page_to_insert})
                            # Let's start our new page
                            if Store_title_in_contents == True:
                                current_page = previous_line
                            pages += 1
                            page_title = previous_line.rstrip()
                            if is_verbose_enough():
                                print("        page title: {}".format(page_title))
                        current_page = current_page + one_line
                        previous_line = one_line
                    if is_verbose_enough():
                        print("      pages: {}".format(pages))
            except:
                print("ERROR - in reading file: {}".format(one_file))
        return ret


def main(conn_string, database, sources):
    source_objs = []
    for source in sources:
        print("Verifying source: {}".format(source))
        repo_type = identify_source(source)
        if repo_type == "docs":
            obj = Docs(source)
        elif repo_type == "training":
            obj = Training(source)
        elif repo_type == "university":
            obj = University(source)

        source_objs.append(obj)

    # Let's create a connection to the MongoDB instance
    # ... clean the previous database and prepare the new collections
    # TODO - allow for only partial updates
    conn = pymongo.MongoClient(conn_string)
    global DB_obj
    DB_obj = conn[database]
    DB_obj.drop_collection(DB_item)
    DB_obj[DB_item].create_index([('contents', pymongo.TEXT)])

    # Let's process all the sources
    for one_source_obj in source_objs:
        one_source_obj.parse()

    sys.exit(Exit_code)


if __name__ == '__main__':
    arguments = docopt(__doc__)
    # Bug in docopt, not handling ':' in a string
    conn_string = arguments['--mongodb']
    if conn_string is None:
        conn_string = "localhost:27017"
    database = arguments['--db']
    Verbose=arguments['--verbose']
    sources=arguments['<source>']
    main(conn_string, database, sources)
