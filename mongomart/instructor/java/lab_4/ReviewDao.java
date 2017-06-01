package mongomart.dao;

import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoCursor;
import com.mongodb.client.MongoDatabase;
import mongomart.model.Review;
import org.bson.Document;
import org.bson.types.ObjectId;

import java.util.ArrayList;
import java.util.List;

import static com.mongodb.client.model.Filters.eq;

/**
 * All database access to the "review" collection
 */
public class ReviewDao {
    private final MongoCollection<Document> reviewCollection;

    /**
     *
     * @param mongoMartDatabase
     */
    public ReviewDao(final MongoDatabase mongoMartDatabase) {
        reviewCollection = mongoMartDatabase.getCollection("review");
    }

    /**
     * Insert a new review
     *
     * @param review User review
     * @return
     */
    public void addReview(Review review) {
        reviewCollection.insertOne(reviewToDoc(review));
    }

    /**
     * Get number of reviews for an item
     *
     * @param itemid itemid to calculate the number of reviews for
     * @return
     */
    public int numReviews(int itemid) {
        return (int)reviewCollection.count(eq("itemid", itemid));
    }

    /**
     * Calculate the average number of stars per itemid
     *
     * @param itemid itemid to calculate average number of stars for
     */

    public int avgStars(int itemid) {
        double returnValue = 0.0;

        // Create an aggregate query for average number of stars
        // db.review.aggregate({ $group : { "_id" : "$productid", "avg_stars" : { "$avg": "$stars" } } })
        Document matchStage = new Document( "$match", new Document("itemid", itemid));
        Document groupStage = new Document( "$group",
                                    new Document( "_id", "$itemid")
                                    .append("avg_stars", new Document("$avg", "$stars")));

        List<Document> aggregateStages = new ArrayList<Document>();
        aggregateStages.add(matchStage);
        aggregateStages.add(groupStage);

        MongoCursor<Document> cursor = reviewCollection.aggregate(aggregateStages, Document.class).useCursor(true).iterator();

        while (cursor.hasNext()) {
            Document resultDoc = cursor.next();
            returnValue = resultDoc.getDouble("avg_stars");
        }

        return (int)returnValue;
    }

    /**
     * Convert a Review object to a document
     *
     * @param review
     * @return
     */
    public static Document reviewToDoc(Review review) {
        Document document = new Document();
        document.append("_id", new ObjectId());
        document.append("name", review.getName());
        document.append("date", review.getDate());
        document.append("comment", review.getComment());
        document.append("stars", review.getStars());
        document.append("itemid", review.getItemid());
        return document;
    }
}
