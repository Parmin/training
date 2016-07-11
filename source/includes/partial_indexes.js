// Putting partial indexes javascript here.
//
//

  { "_id" : 7, "integer" : 7, "importance" : "high" }


// Partial Indexes vs. Sparse Indexes
db.integers.createIndex(
  { integer : 1 },
  { partialFilterExpression : { importance : "high" },
  name : "high_importance_integers" } )
  

// Partial vs. Sparse Indexes Example
db.integers.createIndex(
    { importance : 1 },
    { partialFilterExpression : { importance : { $exists : true } } } 
    )  // similar to a sparse index


// Quiz -- queries and Partial Indexes
db.things.find( { last_update : { $gte : ISODate("2016-01-01") } } )
db.things.find( { last_update : { $gte : ISODate("2015-01-01") } } )


// partial filter example in answer
{ last_update : { $gte : ISODate("2015-01-01") } }


// Identifying partial indexes
> db.integers.getIndexes()
[
...,
  {
    "v" : 1,
    "key" : {
      "integer" : 1
    },
    "name" : "high_importance_integers",
    "ns" : "test.integers",
    "partialFilterExpression" : {
      "importance" : "high"
    }
  },
  ...
]


// No double index coverage example
db.foo.drop()
db.foo.createIndex( { a : 1, b : -1 },
        { partialFilterExpression : { a : { $gte : 100000 } } } )  // works
db.foo.createIndex( { a : 1, b : -1  },
        { partialFilterExpression : { a : { $lte : 100000 } } } )  // fails


// Hinting done wrong
db.foo.drop()
docs = []; for (i=1; i<=10; i++) {
  docs.push( {
      student_id: i,
      score : Math.random(),
      subject_name: "english" } )
}; db.foo.insertMany( docs )
docs = []; for (i=1; i<=10; i++) {
  docs.push( {
      student_id: i,
      score : Math.random(),
      subject_name: "mathematics" } )
}; db.foo.insertMany( docs )
db.foo.createIndex( { score : 1 },
   { partialFilterExpression : { subject_name: "english" } } )
db.foo.find( { score : { $gte : 0.5 } } )
// that worked fine, but did a collection scan
db.foo.find( { score : { $gte : 0.5 } } ).hint( { score: 1 } )
// missed documents


// Quiz: partialFilterExpression
{
  "v" : 1,
  "key" : {
    "score" : 1,
    "student_id" : 1
  },
  "name" : "score_1_student_id_1",
  "ns" : "test.scores",
  "partialFilterExpression" : {
    "score" : {
      "$gte" : 0.65
    },
    "subject_name" : "history"
  }
}


// Quiz which documents are indexed
{ "_id" : 1, "student_id" : 2, "score" : 0.84, "subject_name" : "history" }
{ "_id" : 2, "student_id" : 3, "score" : 0.57, "subject_name" : "history" }
{ "_id" : 3, "student_id" : 4, "score" : 0.56, "subject_name" : "physics" }
{ "_id" : 4, "student_id" : 4, "score" : 0.75, "subject_name" : "physics" }
{ "_id" : 5, "student_id" : 3, "score" : 0.89, "subject_name" : "history" }

