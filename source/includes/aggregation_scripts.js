// Mongo shell scripts for aggregation
//

// $sample example
db.companies.aggregate( [
     { $sample : { size : 5 } },
     { $project : { _id : 0, number_of_employees: 1 } }
] )

// $indexStats example
db.companies.dropIndexes()
db.companies.createIndex( { number_of_employees : 1 } )
db.companies.aggregate( [ { $indexStats: {} } ] )
db.companies.find( { number_of_employees : { $gte : 100 } },
                   { number_of_employees: 1 } ).next()
db.companies.find( { number_of_employees : { $gte : 100 } },
                   { number_of_employees: 1 } ).next()
db.companies.aggregate( [ { $indexStats: {} } ] )


// $lookup example
db.commentOnEmployees.insertMany( [
    { employeeCount: 405000,
      comment: "Biggest company in the set." },
    { employeeCount: 405000,
      comment: "So you get two comments." },
    { employeeCount: 100000,
      comment: "This is a suspiciously round number." },
    { employeeCount: 99999,
      comment: "This is a suspiciously accurate number." },
    { employeeCount: 99998,
      comment: "This isn't in the data set." }
    ] )
db.companies.aggregate( [
  { $match: { number_of_employees: { $in:
      [ 405000, 388000, 100000, 99999, 99998 ] } } },
  { $project: { _id :0, name: 1, number_of_employees: 1 } },
  { $lookup: {
      from: "commentOnEmployees",
      localField: "number_of_employees",
      foreignField: "employeeCount",
      as: "example_comments"
  } },
  { $sort : { number_of_employees: -1 } } ] )


// $stdevpop example
db.companies.aggregate( [
{ $match : { number_of_employees: { $lt: 1000, $gte: 100 } } },
{ $group : {
    _id : null,
    mean_employees: { $avg : "$number_of_employees" },
    std_num_employees : { $stdDevPop: "$number_of_employees" } } }
] )


// $trunc example
db.companies.aggregate( [
  { $match : { number_of_employees: { $gte: 100, $lt: 1000 } } },
  { $group : { _id : null,
               mean_employees: { $avg: "$number_of_employees" } } },
  { $project : { _id: 0,
                 truncated_mean_employees: { $trunc : "$mean_employees" } } }
   ] )


// $filter example
db.companies.aggregate( [
  { $match : { "funding_rounds.round_code": "e" } },
  { $project : {
      _id: 0, name: 1,
      series_e_funding: {
        $filter: {
          input: "$funding_rounds",
          as: "series_e_funding",
          cond: { $eq : [ "$$series_e_funding.round_code", "e" ] } } } }
  }, {
    $project : {
      name: 1,
      "series_e_funding.raised_amount": 1,
      "series_e_funding.raised_currency_code": 1,
      "series_e_funding.year": 1 }
  } ] )


// $project accumulators example
db.foo.drop()
db.foo.insertMany( [ { numbers: [ 1, 2, 3, 4, 5 ] },
                     { numbers: [ 6, 7, 8, 9, 10 ] } ] )
db.foo.aggregate( [
  {
    $project: {
      _id: 0,
      avg: { $avg: "$numbers" },
      sum: { $sum: "$numbers" },
      min: { $min: "$numbers" },
      max: { $max: "$numbers" },
      stDevSamp: { $stdDevSamp: "$numbers" } }
  } ] )
db.foo.find( {}, { _id: 0 } )  // these are the original documents


// $projecting arrays example
db.plants.drop()
db.plants.insertMany( [
  { _id: "yellow plants", fruit: "banana", vegetable: "squash" },
  { _id: "red plants", fruit: "strawberry", vegetable: "radish" } ] )
db.plants.aggregate( [ { $project: { plant_list: [ "$fruit", "$vegetable" ] } } ] )
