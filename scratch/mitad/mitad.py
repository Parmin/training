#!/usr/bin/env python3

"""
Construct a catalog of some MongoDB knowledge from different sources.

Usage:
    mitad -h
    mitad [--verbosity=<N>] [--mongodb=<conn_string>] [--db=<database>] <source> ...

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
    -v --verbosity=<N>      Print more information about the processing, from none (0) to max (5) [default: 1]
    <source> ...            Sources to process. Those must be paths to a file system

Examples:
    python mitad.py --verbosity 2 ./training-sw ./university-courses-sw ./docs
"""
# end docopt usage string

# implementation notes
"""
- uses "Knowledge Info" tags of the form
    .. KI <key> : <value>
    <key> being "learning_obj", ...
    any <key> will be accepted and added to the document
  in the .txt or .rst files.
  Those line are disregarded by Giza and discarded by Sphinx.

- verbosity
    - 1: high level output, errors
    - 2: warnings
    - 3: list of files
    - 4: actions per files
    - 5: nothing yet, but likely very verbose stuff like being in loops

TODOs:
    - count the number of files processed
    - report all errors encountered at the end
    - report some stats at the end
    - support sources as GitHub refs instead of local repos
    - have 'path' and 'uri'
    - have 'debug' mode to not catch exceptions, and/or only catch specific exceptions
    - pylint
    - report type of error per file, especially 'UnicodeDecodeError'
"""

import glob
import json
import logging
import os
import os.path
import pymongo
import re
import shutil
import subprocess
import sys

from datetime import datetime
from docopt import docopt

DB_obj = None
Exit_Code = 0
Verbosity = 1

# How we store info in the collections
Store_contents_as_array = True
Store_title_in_contents = True

DB_ITEM = 'item'
KI_REGEX = "^\.\. KI\s+(.+?)\s*:\s*(.+)$"   # Matching the KI directives in the files processed by Giza

def clean_filenames(filenames):
    new_filenames = []
    for filename in filenames:
        new_filename = filename.replace("\\", "/")
        new_filenames.append(new_filename)
        return new_filenames

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
        if is_verbose_enough(1):
            print("  Repo type: {}".format(type))
    except:
        raise Exception("FATAL - Can't identify repository type from path {}".format(path))
    return type

def is_verbose_enough(level_needed):
    verbose = False
    if Verbosity >= level_needed:
        verbose = True
    return verbose

def print_exception(ex):
    if is_verbose_enough(1):
        print(type(ex).__name__)
        print(str(ex))
        print()

def run_cmd(cmd):
    cmd_list = cmd.split(" ")
    output = subprocess.Popen(cmd_list, stdout=subprocess.PIPE).communicate()[0]
    return output.decode("utf-8")

'''
Base class for all RST based repositories
'''
class BaseRst(object):
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

    def get_ki(self, one_line):
        ret = (None, None)
        match = re.search(KI_REGEX, one_line)
        if match:
            key = match.group(1)
            value = match.group(2)
            ret = (key, value)
        return ret

    def insert_doc(self, doc):
        DB_obj[DB_ITEM].insert(doc)

    def merge_dicts(self, doc, otherdic):
        for key in otherdic.keys():
            doc[key] = otherdic[key]
        return doc


class Docs(BaseRst):
    def __init__(self, path):
        super().__init__(path)

    def parse(self):
        ret = True
        dirs = ['source/*.txt', 'source/*/*.txt', 'source/reference/*/*.txt']
        files = self.get_files(dirs)
        for one_file in files:
            try:
                # Some files (6?) like "training/source/modules/aggregation.txt" have format isssues, so let's skip them
                if is_verbose_enough(3):
                    print("    File: {}".format(one_file))
                pages = 0
                current_section = ''
                current_page = ''
                page_title = ''
                previous_line = ''
                keywords = []
                kis = dict()
                with open(one_file) as file_obj:
                    if re.match(".*tutorial.*", one_file):
                        knowledge_type = "tutorial"
                    else:
                        knowledge_type = "doc"
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
                                doc = { 'source': 'docs',
                                        'type': knowledge_type,
                                        'path': one_file,
                                        'section': current_section,
                                        'title': page_title,
                                        'keywords': keywords,
                                        'contents': current_page_to_insert }
                                doc = self.merge_dicts(doc, kis)
                                self.insert_doc(doc)
                            # Let's start our new page
                            if Store_title_in_contents == True:
                                current_page = previous_line
                            pages += 1
                            page_title = previous_line.rstrip()
                            kis = dict()
                            if is_verbose_enough(4):
                                print("        page title: {}".format(page_title))
                        (ki_key, ki_value) = self.get_ki(one_line)
                        if ki_key is not None:
                            kis[ki_key] = ki_value
                        current_page = current_page + one_line
                        previous_line = one_line
                    if is_verbose_enough(4):
                        print("      number of pages: {}".format(pages))
            except Exception as ex:
                print("ERROR - in processing file: {}".format(one_file))
                print_exception(ex)

        return ret


class Training(BaseRst):
    def __init__(self, path):
        super().__init__(path)

    def parse(self):
        ret = True
        dirs = ['source/modules/*.txt', 'source/modules/internal/*.txt']
        files = self.get_files(dirs)
        for one_file in files:
            try:
                # Some files (6?) like "training/source/modules/aggregation.txt" have format isssues, so let's skip them
                if is_verbose_enough(3):
                    print("    File: {}".format(one_file))
                pages = 0
                current_section = ''
                current_page = ''
                page_title = ''
                previous_line = ''
                keywords = []
                kis = dict()
                with open(one_file) as file_obj:
                    if re.match(".*internal.*", one_file):
                        knowledge_type = "nhtt"
                    else:
                        knowledge_type = "inperson"
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
                                doc = { 'source': 'training',
                                        'type': knowledge_type,
                                        'path': one_file,
                                        'section': current_section,
                                        'title': page_title,
                                        'keywords': keywords,
                                        'contents': current_page_to_insert }
                                doc = self.merge_dicts(doc, kis)
                                self.insert_doc(doc)
                            # Let's start our new page
                            if Store_title_in_contents == True:
                                current_page = previous_line
                            pages += 1
                            page_title = previous_line.rstrip()
                            kis = dict()
                            if is_verbose_enough(4):
                                print("        page title: {}".format(page_title))
                        (ki_key, ki_value) = self.get_ki(one_line)
                        if ki_key is not None:
                            kis[ki_key] = ki_value
                        current_page = current_page + one_line
                        previous_line = one_line
                    if is_verbose_enough(4):
                        print("      number of pages: {}".format(pages))
            except Exception as ex:
                print("ERROR - in processing file: {}".format(one_file))
                print_exception(ex)

        return ret


class University(BaseRst):
    def __init__(self, path):
        super().__init__(path)

    def parse(self):
        ret = True

        # First pass is to go through all the rst/txt files
        # Then in a second pass, we will add the video captions to the pages seens in the first pass
        dirs = ['src/lessons/*.rst', 'src/lessons/*/*.rst']
        files = self.get_files(dirs)
        for one_file in files:
            try:
                if is_verbose_enough(3):
                    print("    File: {}".format(one_file))
                pages = 0
                current_section = ''
                current_page = ''
                page_title = ''
                previous_line = ''
                video = ''
                keywords = []
                kis = dict()
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
                                doc = { 'source': 'university-course',
                                        'type': 'online',
                                        'path': one_file,
                                        'section': current_section,
                                        'title': page_title,
                                        'video': video,
                                        'keywords': keywords,
                                        'contents': current_page_to_insert }
                                doc = self.merge_dicts(doc, kis)
                                self.insert_doc(doc)
                            # Let's start our new page
                            if Store_title_in_contents == True:
                                current_page = previous_line
                            pages += 1
                            page_title = previous_line.rstrip()
                            kis = dict()
                            video = ''
                            if is_verbose_enough(4):
                                print("        page title: {}".format(page_title))

                        # Looking for a line that points to a video
                        video_match = re.search('<https://youtu.be/(.+)>', one_line, re.IGNORECASE)
                        if video_match:
                            if video != '':
                                if is_verbose_enough(2):
                                    pass
                                    # This is OK to have 2 videos if one is Japanese
                                    #print("WARNING - there is already a video for this page {}".format(one_file))
                            video = video_match.group(1)
                        (ki_key, ki_value) = self.get_ki(one_line)
                        if ki_key is not None:
                            kis[ki_key] = ki_value
                        current_page = current_page + one_line
                        previous_line = one_line
                    if is_verbose_enough(4):
                        print("      number of pages: {}".format(pages))
            except Exception as ex:
                print("ERROR - in processing file: {}".format(one_file))
                print_exception(ex)

        # Second pass, let's process the captions
        dirs = ['src/captions/*.srt']
        files = self.get_files(dirs)
        for one_file in files:
            try:
                # Some files (6?) like "training/source/modules/aggregation.txt" have format isssues, so let's skip them
                if is_verbose_enough(3):
                    print("    File: {}".format(one_file))
                with open(one_file) as file_obj:
                    captions = []
                    time = ''
                    text_at_time = ''
                    # TODO - add some consistency check on the flow of lines.
                    for one_line in file_obj:
                        # Construct a nice array with the captions
                        # and we will add it to the 'contents' of the appropriate page
                        if re.match("^\d+$", one_line):
                            # Skip those lines and complete the previous section
                            if time != '':
                                captions.append("{}: {}".format(time, text_at_time))
                            time = ''
                            text_at_time = ''
                        else:
                            match_timestamp = re.search("^\d\d:(\d\d:\d\d)", one_line)
                            if match_timestamp:
                                time = match_timestamp.group(1)
                            else:
                                text_at_time = text_at_time + " " + one_line.rstrip()
                    # Complete the last part
                    if time != '':
                        captions.append("{}: {}".format(time, text_at_time))
                    # Find the corresponding document for those captions
                    basename = os.path.basename(one_file)
                    video_id = os.path.splitext(basename)[0]
                    doc = DB_obj[DB_ITEM].find_one({'video': video_id})
                    if doc is None:
                        if is_verbose_enough(2):
                            print("WARNING - Can't find a document to associate this video to {}".format(video_id))
                    else:
                        DB_obj[DB_ITEM].update_one({"_id": doc['_id']}, {'$push': {'contents': { '$each': captions }}})

            except Exception as ex:
                print("ERROR - in processing file: {}".format(one_file))
                print_exception(ex)

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
    # We could consider partial update by keeping checksums on files,
    # however the processing is so fast, that it is not worth the investment
    # at this point.
    conn = pymongo.MongoClient(conn_string)
    global DB_obj
    DB_obj = conn[database]
    DB_obj.drop_collection(DB_ITEM)
    DB_obj[DB_ITEM].create_index([('contents', pymongo.TEXT)])
    DB_obj[DB_ITEM].create_index([('learning_obj', pymongo.ASCENDING)])

    # Let's process all the sources
    for one_source_obj in source_objs:
        one_source_obj.parse()

    sys.exit(Exit_Code)


if __name__ == '__main__':
    arguments = docopt(__doc__)
    # Bug in docopt, not handling ':' in a string
    conn_string = arguments['--mongodb']
    if conn_string is None:
        conn_string = "localhost:27017"
    database = arguments['--db']
    Verbosity = int(arguments['--verbosity'])
    sources = arguments['<source>']
    main(conn_string, database, sources)
