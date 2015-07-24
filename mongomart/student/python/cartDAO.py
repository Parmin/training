#
# All database access to the "cart" collection
#

import sys
import random
import string
import datetime

__author__ = 'jz'

class CartDAO:

    def __init__(self, database):
        self.db = database

    # Get a cart by userid
    def get_cart(self, userid):

        #
        # TODO-lab2
        #
        # LAB #2: Query the "cart" collection by userid and return a Cart object.
        #

        cart = {}
        cart['_id'] = 1
        cart['userid'] = userid
        items = []
        item = {}
        item['_id'] = 1
        item['title'] = "Gray Hooded Sweatshirt"
        item['category'] = "Apparel"
        item['quantity'] = 1
        item['price'] = 29.99
        item['img_url'] = "/img/products/hoodie.jpg"
        items.append(item)

        cart['items'] = items

        # TODO-lab2 Replace all code above (dummy code used to populate fake cart)

        return cart

    # Add an item to a cart
    def add_item(self, userid, item):
        #
        # TODO-lab2
        #
        # LAB #2: Add an item to a user's cart document
        #
        # HINT: There are several cases you must account for here, such as an empty initial cart
        #
        print "Item added to cart"

    # Update the quantity of an item in a cart.  If quantity is 0, remove item from cart
    def update_quantity(self, userid, itemid, quantity):
        #
        # TODO-lab2
        #
        # LAB #2: Update the quantity of an item in a users cart, if the quantity is 0, remove the item from the cart
        #
        # HINT: You may want to create a helper method for determining if an item already exists in a cart
        #
        print "Quantity in cart updated"
    