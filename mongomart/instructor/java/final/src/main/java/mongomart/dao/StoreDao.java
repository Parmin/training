package mongomart.dao;

import com.mongodb.BasicDBObject;
import com.mongodb.DBCursor;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoCursor;
import com.mongodb.client.MongoDatabase;
import mongomart.model.Store;
import org.bson.Document;

import java.util.*;

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

    public List<Store> getAllStores() {
        try (MongoCursor<Document> cursor = collection.find()
                .sort(orderBy(ascending("name")))
                .iterator()) {
            List<Store> stores = new ArrayList<>();
            while (cursor.hasNext()) {
                stores.add(buildStore(cursor.next()));
            }
            return stores;
        }
    }

    public Store getStoreWithStoreId(final String storeId) {
        Document doc = collection.find(eq("storeId", storeId)).first();
        if (doc == null) {
            return null;
        }
        return buildStore(doc);
    }

    public List<Store> getStoresWithCity(final String city) {
        try (MongoCursor<Document> cursor = collection.find(eq("city", city))
                .sort(orderBy(ascending("name")))
                .iterator()) {
            List<Store> stores = new ArrayList<>();
            while (cursor.hasNext()) {
                stores.add(buildStore(cursor.next()));
            }
            return stores;
        }
    }

    public List<Store> getStoresWithZip(final String zip) {
        try (MongoCursor<Document> cursor = collection.find(eq("zip", zip))
                .sort(orderBy(ascending("name")))
                .iterator()) {
            List<Store> stores = new ArrayList<>();
            while (cursor.hasNext()) {
                stores.add(buildStore(cursor.next()));
            }
            return stores;
        }
    }

    public List<Store> getStoresClosestToZip(final String zipCode) {
        Document doc = zipCollection.find(eq("_id", zipCode)).first();
        if (doc == null) {
            return new ArrayList<Store>();
        }
        List<Double> location = (List<Double>) doc.get("loc");
        return getStoresClosestToLocation(location.get(0), location.get(1));
    }

    public List<Store> getStoresClosestToLocation(final double longitude, final double latitude) {
        List<Document> pipeline = buildClosestToLocationPipeline(longitude, latitude);

        try (MongoCursor<Document> cursor = collection.aggregate(pipeline).iterator()) {
            List<Store> stores = new ArrayList<>();
            while (cursor.hasNext()) {
                stores.add(buildStore(cursor.next()));
            }
            return stores;
        }
    }

    private List<Document> buildClosestToLocationPipeline(final double longitude, final double latitude) {
        // Documents are already sorted
        Document geoNear = new Document(
                "$geoNear",
                new Document(
                        "near",
                        new Document("type", "Point")
                                .append("coordinates", new double[] { longitude, latitude })
                )
                        .append("distanceField", "dist.calculated")
                        .append("spherical", "true")
                        .append("distanceMultiplier", 0.001)
        );

        List<Document> pipeline = new ArrayList<Document>();
        pipeline.add(geoNear);
        return pipeline;
    }

    private static Store buildStore(Document document) {
        // TODO: should this use a builder pattern?
        return new Store(
                document.getObjectId("_id"), document.getString("storeId"), document.getString("name"),
                document.getDouble("longitude"), document.getDouble("latitude"), document.getString("address"),
                document.getString("address2"), document.getString("city"), document.getString("state"),
                document.getString("zip"), document.getString("country")
        );
    }
}
