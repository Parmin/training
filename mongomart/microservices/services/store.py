#!/usr/local/bin/python
from bottle import response, request
import bottle
import pymongo

_allow_origin = '*'
_allow_methods = 'PUT, GET, POST, DELETE, OPTIONS'
_allow_headers = 'Authorization, Origin, Accept, Content-Type, X-Requested-With'


#your methods should go here


db = pymongo.MongoClient().store
bottle.debug(True)
# Start the webserver running and wait for requests
bottle.run(host='localhost', port=9084)
