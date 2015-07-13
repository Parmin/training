
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
import math

from bottle import route, request, response, template



__author__ = 'jz'


# CONSTANTS
ITEMS_PER_PAGE = 5

@bottle.route('/static/:filename#.*#')
def send_static(filename):
    return bottle.static_file(filename, root='./static/')

@bottle.route('/')
def index():
    page = request.query.page or 0
    category = request.query.category or 'All'

    categories = items.get_categories()
    all_items = items.get_items(category, int(page), ITEMS_PER_PAGE)
    item_count = items.get_num_items(category)

    num_pages = 0;
    if item_count > ITEMS_PER_PAGE:
        num_pages = int(math.ceil(item_count / ITEMS_PER_PAGE))

    return bottle.template('home', dict(category_param=category, 
                                        categories=categories, 
                                        useRangeBasedPagination=False,
                                        item_count=item_count,
                                        pages=num_pages,
                                        page=int(page),
                                        items = all_items
                                        ))

@bottle.route('/search')
def search():
    page = request.query.page or 0
    query = request.query.query or ''

    search_items = items.search_items(query, int(page), ITEMS_PER_PAGE)
    item_count = items.get_num_search_items(query)

    num_pages = 0;
    if item_count > ITEMS_PER_PAGE:
        num_pages = int(math.ceil(item_count / ITEMS_PER_PAGE))

    return bottle.template('search', dict(query_string=query,
                                        item_count=item_count,
                                        pages=num_pages,
                                        page=int(page),
                                        items = search_items
                                        ))

@bottle.route('/item')
def item():
    itemid = request.query.id
    
    item = items.get_item(int(itemid))

    num_reviews = len(item['reviews'])
    stars = 0
    for review in item['reviews']:
        stars += review['stars']

    if ( num_reviews > 0 ): 
        stars = stars / num_reviews

    related_items = items.get_related_items()

    return bottle.template('item', dict(item = item,
                                        stars = stars,
                                        num_reviews = num_reviews,
                                        related_items = related_items
                                        ))

@bottle.route('/add-review')
def add_review():
    itemid = request.query.itemid
    review = request.query.review
    name = request.query.name
    stars = int(request.query.stars)

    item = items.add_review(itemid, review, name, stars)

    return bottle.redirect("/item?id=" + str(itemid))

connection_string = "mongodb://localhost"
connection = pymongo.MongoClient(connection_string)
database = connection.mongomart

items = itemDAO.ItemDAO(database)


bottle.debug(True)
bottle.run(host='localhost', port=8082)         # Start the webserver running and wait for requests

