package mongomart.dao;

import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoCursor;
import com.mongodb.client.MongoDatabase;
import mongomart.config.Utils;
import mongomart.model.Category;
import mongomart.model.Item;
import mongomart.model.Review;
import org.bson.Document;

import java.util.ArrayList;
import java.util.List;

import static com.mongodb.client.model.Filters.*;

/**
 * All database access to the "item" collection
 */
public class ItemDao {
    // Used for pagination
    private static final int ITEMS_PER_PAGE = 5;

    private final MongoCollection<Document> itemCollection;

    /**
     *
     * @param mongoMartDatabase
     */
    public ItemDao(final MongoDatabase mongoMartDatabase) {
        itemCollection = mongoMartDatabase.getCollection("item");
    }

    /**
     * Get an Item by id
     *
     * @param id
     * @return
     */
    public Item getItem(int id) {
        Document itemDoc = itemCollection.find(eq("_id", id)).first();

        // Map document to Item class
        Item item = docToItem(itemDoc);

        /**
         * lab5 - SECTION REMOVED, calculating number of stars when each review is added
         */
        // get average number of stars
        /*
        if (item.getReviews() != null) {
            int num_reviews = 0;
            int total_stars = 0;

            for (Review review : item.getReviews()) {
                num_reviews++;
                total_stars += review.getStars();
            }

            if (num_reviews > 0) {
                item.setStars((int)total_stars / num_reviews);
            }
        }
        */

        return item;
    }

    /**
     * Get items by page number
     *
     * @param page_str
     * @return
     */
    public List<Item> getItems(String page_str) {
        int page = Utils.getIntFromString(page_str);

        List<Document> documents = itemCollection.find()
                                        .skip(ITEMS_PER_PAGE * page)
                                        .limit(ITEMS_PER_PAGE)
                                        .into(new ArrayList<>());

        return docToItem(documents);
    }

    /**
     * Get items using range based pagination, using the after value
     *
     * @param after
     * @return
     */
    public List<Item> getItemsRangeBased(String before, String after) {
        List<Document> documents = new ArrayList<>();

        // Only one item is passed in, before or after, formulate query based on that item

        // Use $lte before
        if (before != null && !before.trim().equals("")) {
            int before_int = Utils.getIntFromString(before);

            List<Document> documents_reverse = itemCollection.find( lt("_id", before_int) )
                    .sort( eq("_id", -1) )  // always sort by _id
                    .limit( ITEMS_PER_PAGE + 1 ) // get one more result than we need, to determine if there is a previous page
                    .into(new ArrayList<>());

            // Now we just need to reverse sort the items
            for (int i=(documents_reverse.size()-1); i>= 0; i--) {
                documents.add(documents_reverse.get(i));
            }
        }

        // Use $gte after
        else {
            int after_int = Utils.getIntFromString(after);

            documents = itemCollection.find( gt("_id", after_int) )
                    .sort( eq("_id", 1) )  // always sort by _id
                    .limit( ITEMS_PER_PAGE + 1 ) // get one more result than we need, to determine if there is a next page
                    .into(new ArrayList<>());
        }


        return docToItem(documents);
    }

    /**
     * Get number of items, useful for pagination
     *
     * @return
     */
    public long getItemsCount() {
        return itemCollection.count();
    }

    /**
     * Get items by category, and page (starting at 0)
     *
     * @param category
     * @param page_str
     * @return
     */
    public List<Item> getItemsByCategory(String category, String page_str) {
        ArrayList<Item> items = new ArrayList<>();
        int page = Utils.getIntFromString(page_str);

        List<Document> documents = itemCollection.find(eq("category", category))
                                     .skip(ITEMS_PER_PAGE * page)
                                     .limit(ITEMS_PER_PAGE)
                                     .into(new ArrayList<>());

        return docToItem(documents);
    }

    /**
     * Get number of items in a category, useful for pagination
     *
     * @param category
     * @return
     */
    public long getItemsByCategoryCount(String category) {
        return itemCollection.count(eq("category", category));
    }

    /**
     * Text search, requires the index:
     *      db.item.createIndex( { "title" : "text", "slogan" : "text", "description" : "text" } )
     *
     * @param query_str
     * @param page_str
     * @return
     */
    public List<Item> textSearch(String query_str, String page_str) {
        ArrayList<Item> items = new ArrayList<>();
        int page = Utils.getIntFromString(page_str);

        List<Document> documents = itemCollection.find(text(query_str))
                .skip(ITEMS_PER_PAGE * page)
                .limit(ITEMS_PER_PAGE)
                .into(new ArrayList<>());

        return docToItem(documents);
    }

    /**
     * Get count for text search results, useful for pagination
     *
     * @param query_str
     * @return
     */
    public long textSearchCount(String query_str) {
        return itemCollection.count(text(query_str));
    }

    /**
     * Use aggregation to get a count of the number of products in each category
     *
     * @return
     */
    public ArrayList<Category> getCategoriesAndNumProducts() {
        ArrayList<Category> categories = new ArrayList<>();

        // db.item.aggregate( { $group : { "_id" : "$category", "count" : { "$sum" : 1 } } }, { $sort : { "_id" : 1 } })
        //Document groupStage = new Document("$group",
        //        (new Document( "_id", "$category")).append("count", new Document("$sum", 1)));
        //Document sortStage = new Document("$sort", new Document("_id", 1));
        //db.item.aggregate( [{$sortByCount: '$category'}]
        Document sortByCount = new Document("$sortByCount", "$category");

        List<Document> aggregateStages = new ArrayList<Document>();
        //aggregateStages.add(groupStage);
        //aggregateStages.add(sortStage);
        aggregateStages.add(sortByCount);

        MongoCursor<Document> cursor = itemCollection.aggregate(aggregateStages, Document.class).useCursor(true).iterator();

        int total_count = 0;
        while (cursor.hasNext()) {
            Document resultDoc = cursor.next();
            Category category = new Category(resultDoc.getString("_id"), resultDoc.getInteger("count"));
            categories.add(category);
            total_count += resultDoc.getInteger("count");
        }

        // All category to display at the top of the category list
        categories.add(0, new Category("All", total_count));

        return categories;
    }

    /**
     * Add a review to an item
     *
     * @param itemid
     * @param review
     */
    public void addReview(Review review, int avg_stars, int itemid) {
        // Push review on to reviews array, make sure to limit at 10
        /*
         db.item.update( { "_id" : 1 }, { $set: { "stars" : 4.3 }, $push : { "reviews" : {
            $each : [{ "name" : "Name", "date" : ISODate("2016-06-30T23:27:22.163Z"), "comment" : "here", "stars" : 5 } ],
            $sort : { "date" : -1 },
            $slice : 10
         } } })
        }
        */

        ArrayList<Document> reviews = new ArrayList<>();
        reviews.add(reviewToDoc(review));

        Document pushUpdate = new Document( "$push", new Document("reviews",
                    new Document("$each", reviews)
                         .append("$sort", new Document("date", -1))
                         .append("$slice", 10)
                )).append("$set", new Document("stars", avg_stars));

        itemCollection.updateOne(eq("_id", itemid), pushUpdate);
    }

    /**
     * Return the constant ITEMS_PER_PAGE
     *
     * @return
     */
    public int getItemsPerPage() {
        return ITEMS_PER_PAGE;
    }

    /**
     * Map a list of documents to a list of Items
     *
     * @param documents
     * @return
     */
    private List<Item> docToItem(List<Document> documents) {
        List<Item> returnValue = new ArrayList<Item>();

        for (Document document : documents) {
            returnValue.add(docToItem(document));
        }

        return returnValue;
    }

    /**
     * Map a document to an Item
     *
     * @param document
     * @return
     */
    private Item docToItem(Document document) {
        Item item = new Item();
        item.setId(document.getInteger("_id"));
        item.setTitle(document.getString("title"));
        item.setDescription(document.getString("description"));
        item.setCategory(document.getString("category"));
        item.setPrice(document.getDouble("price"));
        item.setStars(document.getInteger("stars"));
        item.setImg_url(document.getString("img_url"));
        item.setSlogan(document.getString("slogan"));
        if (document.containsKey("quantity")) {
            item.setQuantity(document.getInteger("quantity"));
        }
        if (document.containsKey("reviews") && document.get("reviews") instanceof List) {
            List<Review> reviews = new ArrayList<>();
            List<Document> reviewsList = (List<Document>)document.get("reviews");

            for (Document reviewDoc : reviewsList) {
                Review review = new Review();
                review.setComment(reviewDoc.getString("comment"));
                review.setName(reviewDoc.getString("name"));
                review.setStars(reviewDoc.getInteger("stars"));
                review.setDate(reviewDoc.getDate("date"));
                reviews.add(review);
            }

            item.setReviews(reviews);
        }
        else {
            item.setReviews(new ArrayList<>());
        }

        return item;
    }

    /**
     * Convert a Review object to a document
     *
     * @param review
     * @return
     */
    public static Document reviewToDoc(Review review) {
        Document document = new Document();
        document.append("name", review.getName());
        document.append("date", review.getDate());
        document.append("comment", review.getComment());
        document.append("stars", review.getStars());
        return document;
    }
}
