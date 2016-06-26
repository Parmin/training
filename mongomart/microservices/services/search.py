import bottle
import pymongo

db = {}

@get('/search')
def search_items(query):
    pass




bottle.debug(True)
# Start the webserver running and wait for requests
bottle.run(host='localhost', port=9080)
