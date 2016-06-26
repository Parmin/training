#!/usr/local/bin/python
import bottle
import pymongo

_allow_origin = '*'
_allow_methods = 'PUT, GET, POST, DELETE, OPTIONS'
_allow_headers = 'Authorization, Origin, Accept, Content-Type, X-Requested-With'





db = pymongo.MongoClient().item
bottle.debug(True)
# Start the webserver running and wait for requests
bottle.run(host='localhost', port=9081)
