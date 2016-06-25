__author__ = 'jz'

import sys
import random
import string
import datetime

class ReviewDAO:

    def __init__(self, database):
        self.db = database
        self.review = self.db.review

    def get_avg_stars(self, itemid):
        # TODO lab3 - create an aggregation pipeline to generate the list of categories
        pipeline = []
        categories = list(self.review.aggregate(pipeline))

        print len(categories)

        if len(categories) > 0:
            return categories[0]['avg_stars']

        return 0

    def get_num_reviews(self, itemid):
        num_reviews = self.review.find( { 'itemid' : itemid }).count()

        return num_reviews

    def add_review(self, itemid, review, name, stars):

        self.review.insert( { 'itemid' : int(itemid), 'name' : name, 'comment' : review, 'stars' : stars, 'date' : datetime.datetime.now() } )
