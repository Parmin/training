#!/usr/bin/python
from eve import Eve

item_schema = {
    "id": { "type": "number"},
    "title": { "type": "string",},
    "slogan": { "type": "string"},
    "description": { "type": "string"},
    "stars": { "type": "int"},
    "category": { "type": "string"},
    "img_url": { "type": "string"},
    "price": { "type": "number"}
}

item = {
    "resource_methods": ["GET", "POST"],
    "schema": item_schema,
    "additional_lookup":{
        "url": 'regex("\d+")',
        "field": "id"
    }
}

settings = {
    "X_DOMAINS" : '*' ,
    "MONGO_HOST": "127.0.0.1",
    "MONGO_PORT": 27017,
    "MONGO_DBNAME": "mongomart",
    "DOMAIN":{"item_eve": item}
}

app = Eve(settings=settings)
app.run(port=7080)
