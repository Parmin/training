// for module crud-updating-documents.txt


// replaceOne example
db.movies.insertOne( { title: "Batman" } )
db.movies.find()
db.movies.replaceOne( { title : "Batman" }, { imdb_rating : 7.7 } )
db.movies.find()
db.movies.replaceOne( { imdb_rating: 7.7 }, { title: "Batman", imdb_rating: 7.7 } )    
db.movies.find()
db.movies.replaceOne( { }, { title: "Batman" } )
db.movies.find()  // back in original state
db.movies.replaceOne( { }, { _id : ObjectId() } )



// $set and unset
db.movies.insertMany( [ 
  { 
    "title" : "Batman", 
    "category" : [ "action", "adventure" ], 
    "imdb_rating" : 7.6, 
    "budget" : 35 
  },
  { 
    "title" : "Godzilla", 
    "category" : [ "action", 
    "adventure", "sci-fi" ], 
    "imdb_rating" : 6.6 
  },
  { 
    "title" : "Home Alone", 
    "category" : [ "family", "comedy" ], 
    "imdb_rating" : 7.4 
  }
] )
db.movies.updateOne( { "title" : "Batman" }, { $set : { "imdb_rating" : 7.7 } } )  
db.movies.updateOne( { "title" : "Godzilla" }, { $set : { "budget" : 1 } } ) 
db.movies.updateOne( { "title" : "Home Alone" }, 
                     { $set : { "budget" : 15, "imdb_rating" : 5.5 } } )
db.movies.updateOne( { "title" : "Home Alone" }, { $unset :  { "budget" : 1 } } )


// update operators
db.movies.updateOne( { title: "Batman" }, { $inc: { "imdb_rating" : 2 } } )        
db.movies.updateOne( { title: "Home Alone" }, { $inc: { "budget" : 5 } } )  
db.movies.updateOne( { title: "Batman" }, { $mul: { "imdb_rating" : 4 } } )  
db.movies.updateOne( { title: "Batman" }, 
                     { $rename: { budget: "estimated_budget" } } )
db.movies.updateOne( { title: "Home Alone" }, { $min: { budget: 5 } } )  
db.movies.updateOne( { title: "Home Alone" }, 
                     { $currentDate : { last_updated: { $type: "timestamp" } } } )
// increment movie mentions by 10
db.movie_mentions.updateOne( { title: "E.T." } , 
                             { $inc:  { "mentions_per_hour.5" : 10 } } )                               


// updateMany vs. updateOne
// let's start tracking the number of sequals for each movie
db.movies.updateOne( { }, { $set : { "sequels" : 0 } } )
db.movies.find()
// we need updateMany to change all documents 
db.movies.updateMany( { }, { $set : { "sequels" : 0 } } )
db.movies.find()

