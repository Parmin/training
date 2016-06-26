#!/usr/local/bin/python
import bottle
import pymongo

_allow_origin = '*'
_allow_methods = 'PUT, GET, POST, DELETE, OPTIONS'
_allow_headers = 'Authorization, Origin, Accept, Content-Type, X-Requested-With'

@bootle.post("/cart/<userid>/<itemid>/<quantity>")
def quantity(userid, itemid, quantity):
    if quantity > 0:
        # db.cart.update( { "userid" : "558098a65133816958968d88", "items._id" : 3 }, { $set : { "items.$.quantity" : 5} } )
        db.cart.update_one({ 'userid': userid, 'items._id': itemid },
                             { '$set' : { 'items.$.quantity' : quantity } })

    else:
        # db.cart.update({ "userid" : "558098a65133816958968d88"}, { $pull : { "items" : { "_id" : 1 } } } )
        db.cart.update_one({ 'userid': userid },
                             { '$pull' : { 'items' : { '_id' : itemid }}})

db = pymongo.MongoClient().cart
bottle.debug(True)
# Start the webserver running and wait for requests
bottle.run(host='localhost', port=9080)
