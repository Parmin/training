
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
import cartDAO
import reviewDAO
import bottle
import cgi
import re
import math
import decimal

from bottle import route, request, response, template



__author__ = 'jz'


# CONSTANTS
ITEMS_PER_PAGE = 5
USERID = "558098a65133816958968d88"

@bottle.route('/static/:filename#.*#')
def send_static(filename):
    return bottle.static_file(filename, root='./static/')

@bottle.route('/')
def index():
    page = request.query.page or 0
    category = request.query.category or 'All'

    # for range based pagination
    before = request.query.before or 0
    after = request.query.after or 0

    next_page_url = ''
    previous_page_url = ''

    categories = items.get_categories()
    all_items = items.get_items_range_based(category, int(before), int(after), ITEMS_PER_PAGE)
    item_count = items.get_num_items(category)

    num_items = len(all_items)
    
    if num_items > ITEMS_PER_PAGE:
        # Since we got back one extra item than we needed, we need to trim it
        if before > 0:
            all_items = all_items[1:len(all_items)];
        else:
            all_items = all_items[0:ITEMS_PER_PAGE];
            

    if include_next_page(num_items, before, after):
        next_page_url = '/?category=' + category + '&after=' + str(all_items[len(all_items)-1]['_id'])

    if include_previous_page(num_items, before, after):
        previous_page_url = '/?category=' + category + '&before=' + str(all_items[0]['_id'])

    num_pages = 0;
    if item_count > ITEMS_PER_PAGE:
        num_pages = int(math.ceil(item_count / ITEMS_PER_PAGE))

    return bottle.template('home', dict(category_param=category, 
                                        categories=categories, 
                                        useRangeBasedPagination=True,
                                        item_count=item_count,
                                        pages=num_pages,
                                        page=int(page),
                                        items = all_items,
                                        previous_page_url = previous_page_url,
                                        next_page_url = next_page_url
                                        ))

def include_next_page(num_items, before, after):
    # If homepage, display a next link is number of items is large enough
    if (before == 0 and after == 0 and num_items > ITEMS_PER_PAGE):
        return True
    
    # If only a "before" parameter is passed in
    elif before > 0:
        return True
    
    # Only an "after" parameter was passed in
    elif num_items > ITEMS_PER_PAGE:
        return True
    
    return False

def include_previous_page(num_items, before, after):
    if after > 0:
        return True

    # If only a "before" parameter is passed in
    elif (before > 0 and num_items > ITEMS_PER_PAGE):
        return True
    
    return False

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
    stars = reviews.get_avg_stars(int(itemid))
    num_reviews = reviews.get_num_reviews(int(itemid))

    # Solution for Lab 2 (calculating total reviews and avg stars)
    # 
    # if 'reviews' in item:
    #   num_reviews = len(item['reviews'])
    #
    #    for review in item['reviews']:
    #        stars += review['stars']
    #
    #    if ( num_reviews > 0 ): 
    #        stars = stars / num_reviews

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
    reviews.add_review(itemid, review, name, stars)

    return bottle.redirect("/item?id=" + str(itemid))

@bottle.route('/cart')
def cart():
    return cart_helper(False)   
    
def cart_helper(updated):
    user_cart = cart.get_cart(USERID)
    total = 0
    for item in user_cart['items']:
        total += item['price'] * item['quantity']

    return bottle.template('cart', dict(updated=updated,
                                        cart=user_cart,
                                        total=total
                                        ))    

@bottle.route('/cart/add')
def cart():
    itemid = request.query.itemid
    item = items.get_item(int(itemid))

    cart.add_item(USERID, item)
    
    return cart_helper(True)

@bottle.route('/cart/update')
def update_cart():
    itemid = request.query.itemid
    quantity = request.query.quantity

    cart.update_quantity(USERID, int(itemid), int(quantity))

    return cart_helper(True)

# connection string should contain multiple host names
# e.g. MongoClient('mongodb://localhost:27017,localhost:27018/?replicaSet=rs0')

connection_string = "mongodb://localhost"
connection = pymongo.MongoClient(connection_string, replicaset='rs0', w='majority')
database = connection.mongomart

items = itemDAO.ItemDAO(database)
cart = cartDAO.CartDAO(database)
reviews = reviewDAO.ReviewDAO(database)


bottle.debug(True)
bottle.run(host='localhost', port=8080)         # Start the webserver running and wait for requests

