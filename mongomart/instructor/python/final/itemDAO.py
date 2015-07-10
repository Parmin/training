__author__ = 'aje'


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


# The session Data Access Object handles interactions with the sessions collection

class ItemDAO:

    def __init__(self, database):
        self.db = database
        self.item = self.db.item

    # will start a new session id by adding a new document to the sessions collection
    # returns the sessionID or None
    def get_categories(self):

        categories = []
        categories.append( {'name': 'Jason', 'num_items': 1234 } )

        # db.item.aggregate( { $group : { "_id" : "$category", "num" : { "$sum" : 1 } } }, { $sort : { "_id" : 1 } })
        pipeline = [ { "$group" : { "_id" : "$category", "num" : { "$sum" : 1 } } },
                     { "$sort" : { "_id" : 1 } } ]
        categories = list(self.item.aggregate(pipeline))
        
        return categories

    # will start a new session id by adding a new document to the sessions collection
    # returns the sessionID or None
    def get_items(self):

        items = list(self.item.find().limit(5))
        
        return items
