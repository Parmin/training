#!/usr/local/bin/python
#-*- coding: utf-8 -*-
import tornado.escape
import tornado.ioloop
import tornado.web
from tornado.httpclient import AsyncHTTPClient
from pymongo import MongoClient, TEXT
from datetime import datetime
import time


class FTSHandler(tornado.web.RequestHandler):

    def initialize(self, collection):
        self._coll = collection

    def format_response(self, item):
        pass

    def get(self, term):
        cur = self._coll.find( {"$text": {"$search": term, "$language": 'english'}})

        docs = []
        for item in cur:
            docs.append(item)

        self.write({'result':docs})


class SearchTermHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def get(self, term):
        page = request.query.page or 0
        query = request.query.query or ''
        AsyncHTTPClient().fetch(
                'http://localhost:8181/fts/{0}'.format(term),
                callback=self.on_response
                );

    def on_response(self, response):

        response = dict(items = response['result'])

        self.write(doc_response)
        self.finish()


uri = "mongodb://localhost:27017"
databasename = 'mongomart'
mc = MongoClient(uri)
db = mc[databasename]

urls = [
        (r"/search/([^/]+)", SearchTermHandler),
        (r"/fts/([^/]+)", FTSHandler, dict(collection=db.item)),
        ]
app = tornado.web.Application(urls)

if __name__ == '__main__':
    app.listen(8181)
    tornado.ioloop.IOLoop.instance().start()
