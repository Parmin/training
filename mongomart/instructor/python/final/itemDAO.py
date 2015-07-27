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
import pymongo


# The session Data Access Object handles interactions with the sessions collection

class ItemDAO:

    def __init__(self, database):
        self.db = database
        self.item = self.db.item

    # will start a new session id by adding a new document to the sessions collection
    # returns the sessionID or None
    def get_categories(self):

        # db.item.aggregate( { $group : { "_id" : "$category", "num" : { "$sum" : 1 } } }, { $sort : { "_id" : 1 } })
        pipeline = [ { "$group" : { "_id" : "$category", "num" : { "$sum" : 1 } } },
                     { "$sort" : { "_id" : 1 } } ]
        categories = list(self.item.aggregate(pipeline))

        total = 0
        for category in categories:
            total += category['num']

        categories.insert(0,  {'_id': 'All', 'num': total } )
        
        return categories

    def get_items(self, category, page, items_per_page):

        if category == 'All':
            items = list(self.item.find().skip(int(page*items_per_page)).limit(items_per_page))
        else:
            items = list(self.item.find( { 'category' : category }).skip(int(page*items_per_page)).limit(items_per_page))
        
        return items

    def get_items_range_based(self, before, after, items_per_page):

        if before > 0:
            items = list(self.item.find( { '_id' : { '$lt' : before }}).sort( '_id' , pymongo.DESCENDING).limit(items_per_page + 1))

            #reverse order of results
            items.reverse()
        else:
            items = list(self.item.find( { '_id' : { '$gt' : after }}).sort( '_id' , pymongo.ASCENDING).limit(items_per_page + 1))

        return items

    def get_num_items(self, category):
        num_items = 0;

        if category == 'All':
            num_items = self.item.find().count()
        else:
            num_items = self.item.find( { 'category' : category }).count()
        
        return num_items

    def search_items(self, query, page, items_per_page):

        if query == '':
            items = list(self.item.find().skip(int(page*items_per_page)).limit(items_per_page))
        else:
            items = list(self.item.find( { '$text' : { '$search': query } }).skip(int(page*items_per_page)).limit(items_per_page))
        
        return items

    def get_num_search_items(self, query):
        num_items = 0;

        if query == '':
            num_items = self.item.find().count()
        else:
            num_items = self.item.find( { '$text' : { '$search': query } }).count()

        return num_items

    def get_item(self, itemid):
        item = self.item.find_one( { '_id' : itemid })

        return item

    def get_related_items(self):
        items = list(self.item.find().limit(4))
        
        return items

    def add_review(self, itemid, review, name, stars):
        # Push review on to reviews array, make sure to limit at 10
        #
        #  db.item.update( { "_id" : 1 }, { $set: { "stars" : 4.3 }, $push : { "reviews" : {
        #    $each : [{ "name" : "Name", "date" : ISODate("2016-06-30T23:27:22.163Z"), "comment" : "here", "stars" : 5 } ],
        #    $sort : { "date" : -1 },
        #    $slice : 10
        #       } } })
        #   }

        self.item.update({ '_id' : int(itemid) }, 
                         { '$push' : { 
                            'reviews' : { 
                                '$each': [ { 'name' : name, 'comment' : review, 'stars' : stars, 'date' : datetime.datetime.now() } ],
                                '$sort': { "date" : -1 },
                                '$slice': 10
                            }
                        } })
