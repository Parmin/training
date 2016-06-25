Import the item dataset for MongoMart
=====================================

From the console shell, import the item dataset using `mongoimport`:

```shell
$ mongoimport -d mongomart -c item items.json
```

Then from the mongoshell, create a text index on the `item` collection:

```javascript
> use mongomart
> db.item.createIndex( { "title" : "text", "slogan" : "text", "description" : "text" } )
```

Import the store dataset for MongoMart
=====================================

N.B. The store locations dataset is based on Best Buy locations.

From the console shell, import the store dataset using `mongoimport`:

```shell
$ mongoimport -d mongomart -c store stores.json
```

Then from the mongoshell, create some indexes on the `store` collection.

```javascript
> use mongomart
> db.store.createIndex( { "storeId" : 1 }, { "unique": true } );
> db.store.createIndex( { "zip": 1 } );
> db.store.createIndex( { "city": 1 } );
> db.store.createIndex( { "coords": "2dsphere" } );
```

Import the zip dataset for MongoMart
=====================================

From the console shell, import the zip dataset using `mongoimport`:

```shell
$ mongoimport -d mongomart -c zip zips.json
```
