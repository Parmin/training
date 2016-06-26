#!/usr/local/bin/python
from bottle import response, request
import bottle
import pymongo
import json

_allow_origin = '*'
_allow_methods = 'PUT, GET, POST, DELETE, OPTIONS'
_allow_headers = 'Authorization, Origin, Accept, Content-Type, X-Requested-With'


@bottle.get("/")
def hello():
    return "all systems up!"

@bottle.get("/search/<query>")
def search(query):
    cur = db.item.find( {"$text": {"$search": query, "$language": 'english'}})
    docs = []
    for item in cur:
        docs.append(item)

    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'
    return json.dumps({'result':docs})

uri="mongodb://mongosearch:27017"
db = pymongo.MongoClient(uri).mongomart
bottle.debug(True)
# Start the webserver running and wait for requests
bottle.run(host='0.0.0.0', port=8080, debug=True)
