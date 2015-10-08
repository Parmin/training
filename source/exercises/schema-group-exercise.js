{
    _id: ObjectId(),
    name: "MongoDB Logo T-Shirt",
    current_price: 14.99,
    price_history: [ { price: 10.99, changed: ISODate() },
		     { price: 11.99, changed: ISODate() },
		     { price: 12.99, changed: ISODate() } ],
    parent_category: "Shirts",
    ancestor_categories: [ "Apparel", "Mens", "Shirts" ],
    tags: [ { key: "Color", value: "gray" },
	    { key: "Size", value: "Large" } ],
    top_reviews: [
	{ review: "I love this shirt.",
	  upvotes: 30,
	  downvotes: 3,
	  comments: [
	      "totally agree",
	      "my favorite shirt" ] },
	    ...
    ]
}


> db.item.findOne()
{
    _id: "301671", // main item id
    department: "Shoes",
    category: "Shoes/Women/Pumps",
    brand: "Guess",
    thumbnail: "http://cdn…/pump.jpg",
    image: "http://cdn…/pump1.jpg", // larger version of thumbnail
    title: "Evening Platform Pumps",
    description: "Those evening platform pumps put the perfect finishing touches on your most glamourous night-on-the-town outfit",
    shortDescription: "Evening Platform Pumps",
    style: "Designer",
    type: "Platform",
    rating: 4.5, // user rating
    lastUpdated: Date("2014/04/01"), // last update time
    …
}

> db.variant.findOne()
{ 
	_id: "730223104376", // the sku
	itemId: "301671", // references item id
	thumbnail: "http://cdn…/pump-red.jpg", // variant specific
	image: "http://cdn…/pump-red.jpg",
	size: 6.0,
	color: "Red",
	width: "B",
	heelHeight: 5.0,
	lastUpdated: Date("2014/04/01"), // last update time
	… 
}


// summaries
{
    "_id": "p39",
    "title": "Evening Platform Pumps 39",
    "department": "Shoes", "category": "Shoes/Women/Pumps",
    "thumbnail": "http://cdn…/pump-small-39.jpg", "image": "http://cdn…/pump-39.jpg",
    "price": 145.99,
    "rating": 0.95,
    "attrs": [ { "brand" : "Guess"}, … ],
    "sattrs": [ { "style" : "Designer"} ,
		{ "type" : "Platform"}, …],
    "vars": [
	{ "sku": "sku2441",
	  "thumbnail": "http://cdn…/pump-small-39.jpg.Blue",
	  "image": "http://cdn…/pump-39.jpg.Blue",
	  "attrs": [ { "size": 6.0 }, { "color": "Blue" }, …], 
	  "sattrs": [ { "width" : "B"} , { "heelHeight" : 5.0 }, …],
	},
	… Many more skus … ]
}


{ 
    “_id”: “30671”,
    “title”: “Evening Platform Pumps”,
    “department”: “Shoes”,
    “Category”: “Women/Shoes/Pumps”,
    “price”: 149.95,
    “attrs”: [“brand”: “Calvin Klein”, …],
    “sattrs”: [“style”: ”Designer”, …],
    “vars”: [
	{
	    “sku”: “93284847362823”,
	    “attrs”: [{“size”: 6.0}, {“color”: “red”}, …],
	    “sattrs”: [{“width”: 8.0}, {“heelHeight”: 5.0}, …],
	}, … //Many more SKUs
    ]
}


{
    "_id" : 30671,
    "timestamp": ISODate("2015-05-29T00:00:00.000Z"),
    "metric": "views",
    "values": [ 123, 345, ..., 123 ]
}



/**
 
Views

- Category home
- Item detail

  - Category breadcrumbs
  - Reviews 
  - 

*/
