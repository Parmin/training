__author__ = 'jz'


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
import sys
import random
import string
import datetime


# The session Data Access Object handles interactions with the sessions collection

class CartDAO:

    def __init__(self, database):
        self.db = database
        self.cart = self.db.cart

    def get_cart(self, userid):

        #
        # TODO lab2
        #
        # Get Cart: Query the "cart" collection by userid and return a Cart object.
        #


        return cart

    def add_item(self, userid, item):
        if (self.exists_in_cart(userid, item['_id'])):
            self.cart.update_one({ 'userid': userid, 'items._id': item['_id'] },
                                 { '$inc' : { 'items.$.quantity' : 1 } } )
        else:
            self.cart.update_one({ 'userid': userid },
                                 { '$push' : { "items" : {
                                        '_id' : item['_id'],
                                        'title' : item['title'],
                                        'category' : item['category'],
                                        'price' : item['price'],
                                        'quantity' : 1,
                                        'img_url': item['img_url'],
                                 } } },
                                 upsert=True)

    def update_quantity(self, userid, itemid, quantity):
        if quantity > 0:
            # db.cart.update( { "userid" : "558098a65133816958968d88", "items._id" : 3 }, { $set : { "items.$.quantity" : 5} } )
            self.cart.update_one({ 'userid': userid, 'items._id': itemid },
                                 { '$set' : { 'items.$.quantity' : quantity } })

        else:
            # db.cart.update({ "userid" : "558098a65133816958968d88"}, { $pull : { "items" : { "_id" : 1 } } } )
            self.cart.update_one({ 'userid': userid },
                                 { '$pull' : { 'items' : { '_id' : itemid }}})

    def exists_in_cart(self, userid, itemid):
        count = self.cart.find( { 'userid' : userid, 'items._id' : itemid }).count()

        if (count > 0):
            return True
        else:
            return False
