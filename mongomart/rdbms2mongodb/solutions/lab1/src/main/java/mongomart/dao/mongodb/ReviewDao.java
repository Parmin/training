package mongomart.dao.mongodb;

import static com.mongodb.client.model.Filters.eq;

import java.util.ArrayList;
import java.util.List;

import mongomart.model.Review;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.bson.Document;

import com.mongodb.MongoWriteException;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoCursor;
import com.mongodb.client.MongoDatabase;

/**
 * All database access to the "review" collection
 */
public class ReviewDao {
	private final MongoCollection<Document> reviewCollection;
	private Log log = LogFactory.getLog(ReviewDao.class);
	/**
	 *
	 * @param mongoMartDatabase
	 */
	public ReviewDao(final MongoDatabase mongoMartDatabase) {
		reviewCollection = mongoMartDatabase.getCollection("review");
	}


	/**
	 * Get list of item reviews
	 *
	 * @param itemId
	 * @return
	 */
	public List<Review> getItemReviews(int itemId){
		List<Review> reviews = new ArrayList<Review>();

		// db.review.find({'itemid': X })
		Document query = new Document("itemid", itemId);

		for( Document doc :  this.reviewCollection.find(query)){
			reviews.add(ReviewDao.documentToReview(doc));
		}

		return reviews;
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

		// db.review.aggregate([{"$match": {"itemid": itemid}}, {"$group": {"_id": "$itemid", "avg_stars": {"$avg": "$stars"}}}])
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
	 * Insert a new review
	 *
	 * @param review User review
	 * @return
	 */
	public void addReview(Review ... reviews) {
		for(Review review : reviews){
			try{
				reviewCollection.insertOne(reviewToDoc(review));
			} catch(MongoWriteException ex){
				log.warn("Already there: " + ex.getMessage());
			}
		}
	}

	/**
	 * Convert a Document object to Review
	 * @param doc
	 * @return
	 */
	public static Review documentToReview(Document doc){
		Review review = new Review();
		review.set_Id(doc.getObjectId("_id"));
		review.setId(doc.getInteger("id", -120));
		review.setComment(doc.getString("comment"));
		review.setName(doc.getString("name"));
		review.setStars(doc.getInteger("stars"));
		review.setDate(doc.getDate("date"));
		review.setItemid(doc.getInteger("itemid"));

		return review;
	}


	/**
	 * Convert a Review object to a document
	 *
	 * @param review
	 * @return
	 */
	public static Document reviewToDoc(Review review) {
		Document document = new Document();
		if(review.getId() >= 0){
			document.append("id", review.getId());
		}
		document.append("name", review.getName());
		document.append("date", review.getDate());
		document.append("comment", review.getComment());
		document.append("stars", review.getStars());
		document.append("itemid", review.getItemid());
		if (review.get_Id() != null){
			document.append("_id", review.get_Id());
		}
		return document;
	}
}
