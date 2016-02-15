# Script used to cycle through a list of hosts and issues bad queries
import pymongo

# Host names should be changed to ones used by class
hosts = ['mongodb://ec2-54-198-4-27.compute-1.amazonaws.com:27017', 'mongodb://ec2-54-198-4-27.compute-1.amazonaws.com:27017']

var = 1
while var == 1 :
	for hostn in hosts:

		print "HOST %s" % hostn
		
		conn = pymongo.Connection(hostn)
		db = conn['twitter']

		print "-- Bad query count"
		cursor = db.tweets.find({"source" : "web", "user.name":"Jason"}).count()
		
		print "-- Bad sort"
		cursor = db.tweets.find({"favorited":'false'}).sort("id").skip(10000).limit(10)
		for doc in cursor:
			print ('In the %s.' % (doc['_id']))

		print "-- Bad query case insensitive regex"
		cursor = db.tweets.find({"user.name" : '/Beatriz/i'}).limit(10)
		for doc in cursor:
			print ('In the %s.' % (doc['_id']))

		print "-- $where"
		cursor = db.tweets.find( { "$where" : "this.in_reply_to_user_id == 'Jason'" }).skip(1000).limit(10)
		for doc in cursor:
			print ('In the %s.' % (doc['_id']))	

		print "-- Bad update"
		db.tweets.update({"user.lang":"es"}, { "$set": { "user.lang_string" : "spanish"} }, multi=True)

		conn.close()	
