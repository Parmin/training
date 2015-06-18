Import the item dataset for MongoMart
=====================================

mongoimport -d mongomart -c item items.json

db.item.createIndex( { "title" : "text", "slogan" : "text", "description" : "text" } )

