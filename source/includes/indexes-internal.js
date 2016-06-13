
db.collection.getPlanCache()









// Make some documents, run a query, see the plan cache
for (i=1; i<=10; i++) {
    x = []; for (j=1; j<=10; j++) {
        for (k=1; k<=100; k++) {
            x.push( { a : i, b : j, c : k, _id: (1000 * i + 100 * j + k) } )
        }
    }; db.foo.insertMany(x)
}
db.foo.createIndex( { a : 1 } )
db.foo.createIndex( { c : 1, b : 1, a : 1 } )
db.foo.find( { a : { $lte : 5 } } ).sort( { c : 1 } ) 
pc = db.foo.getPlanCache()
pc.listQueryShapes()
