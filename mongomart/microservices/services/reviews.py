import bottle
import pymongo

_allow_origin = '*'
_allow_methods = 'PUT, GET, POST, DELETE, OPTIONS'
_allow_headers = 'Authorization, Origin, Accept, Content-Type, X-Requested-With'

@bottle.get("/reviews/<itemid>/stars")
def get_stars(itemid):
    review = db.review
    pipeline = pipeline = [ { "$match" : { "itemid" : itemid } },
        { "$group" : { "_id" : "$itemid", "avg_stars" : { "$avg" : "$stars" } } } ]
    categories = list(review.aggregate(pipeline))

    response.headers['Content-Type'] = 'applicatio/json'
    response.headers['Cache-Control'] = 'no-cache'

    return json.dumps({'categories': categories})

@bottle.get("/reviews/<itemid>/count")
def get_stars(itemid):
    pass

def new_review():

@bottle.post("/reviews")
def add_review(self, ):
    try:




@hook('after_request')
def enable_cors():
    '''Add headers to enable CORS'''

    response.headers['Access-Control-Allow-Origin'] = _allow_origin
    response.headers['Access-Control-Allow-Methods'] = _allow_methods
    response.headers['Access-Control-Allow-Headers'] = _allow_headers

uri = "mongodb://localhost:27017"
mc = pymongo.MongoClient(uri)
db = mc.mongomart

bottle.debug(True)
# Start the webserver running and wait for requests
bottle.run(host='localhost', port=9080)
