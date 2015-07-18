package mongomart.dao;

import com.mongodb.BasicDBObject;
import com.mongodb.DBCursor;
import com.mongodb.client.AggregateIterable;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoCursor;
import com.mongodb.client.MongoDatabase;
import mongomart.model.Store;
import org.bson.Document;

import java.util.*;
import java.util.stream.Collectors;

import static com.mongodb.client.model.Filters.and;
import static com.mongodb.client.model.Filters.eq;
import static com.mongodb.client.model.Sorts.orderBy;
import static com.mongodb.client.model.Sorts.ascending;

/**
 * Created by glowe on 6/22/15.
 */
public class StoreDao {
    private final MongoCollection<Document> collection;
    private final MongoCollection<Document> zipCollection;
    private final MongoDatabase database;

    public static class ZipNotFound extends Exception {
        public final String zip;

        public ZipNotFound(final String zip) {
            super();
            this.zip = zip;
        }
    }

    public static class CityAndStateNotFound extends Exception {
        public final String city;
        public final String state;

        public CityAndStateNotFound(final String city, final String state) {
            super();
            this.city = city;
            this.state = state;
        }
    }

    /**
     *
     * @param mongoMartDatabase
     */
    public StoreDao(final MongoDatabase mongoMartDatabase) {
        database = mongoMartDatabase;
        collection = database.getCollection("store");
        zipCollection = database.getCollection("zip");
    }

    public SortedSet<String> getAllStates() {
        try (MongoCursor<String> cursor = zipCollection.distinct("state", String.class).iterator()) {
            SortedSet<String> states = new TreeSet<>();
            while (cursor.hasNext()) {
                states.add(cursor.next());
            }
            return states;
        }
    }

    public List<Store> getStoresClosestToCityAndState(
            final String city, final String state, final int skip, final int limit)
            throws CityAndStateNotFound {
        // Arbitrarily choose a matching location.
        Document doc = zipCollection.find(
                and(eq("city", city.toUpperCase()), eq("state", state))).first();
        if (doc == null) {
            throw new CityAndStateNotFound(city, state);
        }
        List<Double> location = (List<Double>) doc.get("loc");
        return getStoresClosestToLocation(location.get(0), location.get(1), skip, limit);
    }

    public List<Store> getStoresClosestToZip(
            final String zipCode, final int skip, final int limit) throws ZipNotFound {
        Document doc = zipCollection.find(eq("_id", zipCode)).first();
        if (doc == null) {
            throw new ZipNotFound(zipCode);
        }
        List<Double> location = (List<Double>) doc.get("loc");
        return getStoresClosestToLocation(location.get(0), location.get(1), skip, limit);
    }

    private List<Store> getStoresClosestToLocation(
            final double longitude, final double latitude, final int skip, final int limit) {
        List<Document> pipeline = buildClosestToLocationPipeline(longitude, latitude);
        pipeline.add(new Document("$skip", skip));
        pipeline.add(new Document("$limit", limit));
        List<Document> docs = collection.aggregate(pipeline).into(new ArrayList<>());
        return docsToStores(docs);
    }

    public long countStores() {
        return collection.count();
    }

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

    private static Store docToStore(Document document) {
        List<Double> coords = (List<Double>) document.get("coords");
        double longitude = coords.get(0);
        double latitude = coords.get(1);

        double distanceFromPoint = document.containsKey("distanceFromPoint") ?
                document.getDouble("distanceFromPoint") : 0.0;

        return new Store(
                document.getObjectId("_id"), document.getString("storeId"), document.getString("name"),
                longitude, latitude, document.getString("address"),
                document.getString("address2"), document.getString("city"), document.getString("state"),
                document.getString("zip"), document.getString("country"), distanceFromPoint
        );
    }

    private static List<Store> docsToStores(List<Document> documents) {
        return documents.stream().map(StoreDao::docToStore).collect(Collectors.toList());
    }
}
