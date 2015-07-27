
#
# Main MongoMart class
#
# To run:
#      Ensure the dataset from data/ has been imported to your MongoDB instance (instructions located in README.md)
#      Run python mongomart.py
#      Open http://localhost:8080
#

import pymongo
import itemDAO
import cartDAO
import bottle
import cgi
import re
import math
import decimal

from bottle import route, request, response, template

__author__ = 'jz'

# CONSTANTS
ITEMS_PER_PAGE = 5

# Hardcoded USERID (for use with the shopping cart portion)
USERID = "558098a65133816958968d88"

# Serve static files in /static (such as css, images, etc.)
@bottle.route('/static/:filename#.*#')
def send_static(filename):
    return bottle.static_file(filename, root='./static/')

# Homepage and category search route
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

# Perform a text search (through search form field on site)
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

# View an item
@bottle.route('/item')
def item():
    itemid = request.query.id
    
    item = items.get_item(int(itemid))
    stars = 0
    num_reviews = 0

    if 'reviews' in item:
        num_reviews = len(item['reviews'])
    
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

# Add a review to an item
@bottle.route('/add-review')
def add_review():
    itemid = request.query.itemid
    review = request.query.review
    name = request.query.name
    stars = int(request.query.stars)

    item = items.add_review(itemid, review, name, stars)

    return bottle.redirect("/item?id=" + str(itemid))

# View your shopping cart
@bottle.route('/cart')
def cart():
    return cart_helper(False)   

# Helper to display the shopping cart, and whether or nor it has been updated    
def cart_helper(updated):
    user_cart = cart.get_cart(USERID)
    total = 0
    for item in user_cart['items']:
        total += item['price'] * item['quantity']

    return bottle.template('cart', dict(updated=updated,
                                        cart=user_cart,
                                        total=total
                                        ))    

# Add an item to the cart
@bottle.route('/cart/add')
def cart():
    itemid = request.query.itemid
    item = items.get_item(int(itemid))

    cart.add_item(USERID, item)
    
    return cart_helper(True)

# Update the quantity of an item in the cart (updating quantity to 0 is the same as removing)
@bottle.route('/cart/update')
def update_cart():
    itemid = request.query.itemid
    quantity = request.query.quantity

    cart.update_quantity(USERID, int(itemid), int(quantity))

    return cart_helper(True)

#
# TODO-lab1
#
# LAB #1: Create a connection to your MongoDB instance, assign the "mongomart"
#         database to the database variable
#

database = {} 

items = itemDAO.ItemDAO(database)
cart = cartDAO.CartDAO(database)

bottle.debug(True)
# Start the webserver running and wait for requests
bottle.run(host='localhost', port=8080)         

