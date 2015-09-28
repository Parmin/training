Lab 6 Solution
==============

Please type in solution with the class instead of distributing source code.

This exercise gives basic practice using the $geoNear geospatial
operator. In the solution, the pipeline contruction has been factored
to a private helper method, but it could also inlined directly into
getStoresClosestToLocation.


Modify StoreDAO.java
--------------------

- Update getStoresClosestToLocation

```java
    private List<Store> getStoresClosestToLocation(
            final double longitude, final double latitude, final int skip, final int limit) {
        List<Document> pipeline = buildClosestToLocationPipeline(longitude, latitude);
        pipeline.add(new Document("$skip", skip));
        pipeline.add(new Document("$limit", limit));
        List<Document> docs = collection.aggregate(pipeline).into(new ArrayList<>());
        return docsToStores(docs);
    }
```

- Add buildClosestToLocationPipeline method

```java
    private List<Document> buildClosestToLocationPipeline(final double longitude, final double latitude) {
        // Documents are already sorted
        List<Double> coordinates = new ArrayList<>();
        coordinates.add(longitude);
        coordinates.add(latitude);
        long numStores = countStores();

        Document geoNear = new Document(
                "$geoNear",
                new Document(
                        "near",
                        new Document("type", "Point").append("coordinates", coordinates)
                )
                        .append("distanceField", "distanceFromPoint")
                        .append("spherical", true)
                        .append("distanceMultiplier", 0.001)
                        .append("limit", numStores)
            );
        List<Document> pipeline = new ArrayList<>();
        pipeline.add(geoNear);
        return pipeline;
    }
```




