#
# All database access to the "item" collection
#

import sys
import random
import string
import datetime

__author__ = 'jz'

class ItemDAO:

    def __init__(self, database):
        self.db = database

    # Use aggregation to get a count of the number of products in each category
    # Result documents should have "_id" as the category name, "num" as the number of products for that category
    def get_categories(self):

        #
        # TODO-lab2
        #
        # LAB #2: Create an aggregation query to return the total number of items in each category.  The
        #         Category object contains "name" and "num_items".  Remember to include an "All" category
        #         for counting all items in the database.
        #
        # HINT: Test your mongodb query in the shell first before implementing it in Python
        #

        categories = []
        category = {}
        category['_id'] = "All"
        category['num'] = 9999

        categories.append(category)

        # TODO-lab2 Replace all code above
        
        return categories

    def get_items(self, category, page, items_per_page):

        #
        # TODO-lab2
        #
        # LAB #2: Return a list of items from the "item" collection, limit by ITEMS_PER_PAGE and
        #         skip by (page_str * ITEMS_PER_PAGE)
        #
        
        item = self.create_dummy_item()

        items = []
        items.append(item)
        items.append(item)
        items.append(item)
        items.append(item)
        items.append(item)
        
        # TODO-lab2 Replace all code above

        return items

    def get_num_items(self, category):
        num_items = 0;

        #
        # TODO-lab2
        #
        # LAB #2: Count the items in the "item" collection, used for pagination, include the category
        #         in the query if it is passed in
        #
        
        return num_items

    def search_items(self, query, page, items_per_page):

        #
        # TODO-lab2
        #
        # LAB #2: Perform a text search against the item collection, , limit by ITEMS_PER_PAGE and
        #         skip by (page_str * ITEMS_PER_PAGE)
        #

        items = []

        return items

    def get_num_search_items(self, query):
        num_items = 0;

        #
        # TODO-lab2
        #
        # LAB #2: Count the items in the "item" collection based on a text search, used for pagination
        #

        return num_items

    def get_item(self, itemid):
        item = {}

        #
        # TODO-lab2
        #
        # LAB #2: Query the "item" collection by _id and return an item document
        #
        
        item = self.create_dummy_item()

        # TODO-lab2 Replace all code above

        return item

    def get_related_items(self):
        items = []

        #
        # TODO-lab2
        #
        # LAB #2: Query and return 4 items from the item collection
        #
        
        return items

    def add_review(self, itemid, review, name, stars):
        
        #
        # TODO-lab2
        #
        # LAB #2: Add a review to an item document
        #
        # HINT: Remember that reviews are a list within the Item object
        #

        print "Review added"

    # Used to populate dummy data, only useful until Lab #2 is completed
    def create_dummy_item(self):
        item = {}
        item['_id'] = 1
        item['title'] = "Gray Hooded Sweatshirt"
        item['description'] = "The top hooded sweatshirt we offer"
        item['slogan'] = "Made of 100% cotton"
        item['stars'] = 0
        item['category'] = "Apparel"
        item['img_url'] = "/img/products/hoodie.jpg"
        item['price'] = 29.99
        item['reviews'] = []
        return item



