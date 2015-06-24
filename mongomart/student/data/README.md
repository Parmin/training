Import the item dataset for MongoMart
=====================================

mongoimport -d mongomart -c item items.json

db.item.createIndex( { "title" : "text", "slogan" : "text", "description" : "text" } )

Import the store dataset for MongoMart
=====================================

mongoimport -d mongomart -c store stores.json

db.store.createIndex( { "storeId" : 1 }, { "unique": true } );
db.store.createIndex( { "zip": 1 } );
db.store.createIndex( { "city": 1 } );
db.store.createIndex( { "coords": "2dsphere" } );

Import the zip dataset for MongoMart
=====================================

mongoimport -d mongomart -c zip zips.json
