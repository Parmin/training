
#
# Copyright (c) 2008 - 2013 10gen, Inc. <http://10gen.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#



import pymongo
import itemDAO
import bottle
import cgi
import re



__author__ = 'aje'


# General Discussion on structure. This program implements a blog. This file is the best place to start to get
# to know the code. In this file, which is the controller, we define a bunch of HTTP routes that are handled
# by functions. The basic way that this magic occurs is through the decorator design pattern. Decorators
# allow you to modify a function, adding code to be executed before and after the function. As a side effect
# the bottle.py decorators also put each callback into a route table.

# These are the routes that the blog must handle. They are decorated using bottle.py

# This route is the main page of the blog
@bottle.route('/static/:filename#.*#')
def send_static(filename):
    return bottle.static_file(filename, root='./static/')

@bottle.route('/')
def blog_index():

    categories = items.get_categories()
    all_items = items.get_items()

    return bottle.template('home', dict(category_param="All", 
                                        categories=categories, 
                                        items = all_items
                                        ))

connection_string = "mongodb://localhost"
connection = pymongo.MongoClient(connection_string)
database = connection.mongomart

items = itemDAO.ItemDAO(database)


bottle.debug(True)
bottle.run(host='localhost', port=8082)         # Start the webserver running and wait for requests

