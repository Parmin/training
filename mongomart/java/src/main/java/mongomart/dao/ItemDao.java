package mongomart.dao;

import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoCursor;
import com.mongodb.client.MongoDatabase;
import mongomart.model.Category;
import mongomart.model.Item;
import mongomart.model.Review;
import org.bson.Document;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import static com.mongodb.client.model.Filters.eq;

/**
 * Created by jason on 6/9/15.
 */
public class ItemDao {
    private final MongoCollection<Item> itemCollection;

    public ItemDao(final MongoDatabase mongoMartDatabase) {
        itemCollection = mongoMartDatabase.getCollection("item", Item.class);
    }

    public Item getItem(int id) {
        Item item = itemCollection.find(eq("_id", id)).first();

        // get average number of stars
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

        return item;
    }

    public ArrayList<Item> getItems() {
        ArrayList<Item> items = new ArrayList<>();

        MongoCursor<Item> cursor = itemCollection.find().limit(10).iterator();
        while (cursor.hasNext()) {
            items.add(cursor.next());
        }

        return items;
    }

    public ArrayList<Item> getItemsByCategory(String category) {
        ArrayList<Item> items = new ArrayList<>();

        MongoCursor<Item> cursor = itemCollection.find(eq("category", category)).limit(10).iterator();
        while (cursor.hasNext()) {
            items.add(cursor.next());
        }

        return items;
    }

    public ArrayList<Category> getCategoriesAndNumProducts() {
        ArrayList<Category> categories = new ArrayList<>();

        // db.item.aggregate( { $group : { "_id" : "$category", "num" : { "$sum" : 1 } } }, { $sort : { "_id" : -1 } })
        Document groupStage = new Document("$group",
                (new Document( "_id", "$category")).append("num", new Document("$sum", 1)));
        Document sortStage = new Document("$sort", new Document("_id", -1));

        List<Document> aggregateStages = new ArrayList<Document>();
        aggregateStages.add(groupStage);
        aggregateStages.add(sortStage);

        MongoCursor<Document> cursor = itemCollection.aggregate(aggregateStages, Document.class).useCursor(true).iterator();
        while (cursor.hasNext()) {
            Document resultDoc = cursor.next();
            Category category = new Category(resultDoc.getString("_id"), resultDoc.getInteger("num"));
            System.out.println("Category: " + resultDoc.getString("_id") + ", num:" + resultDoc.getInteger("num"));
            categories.add(category);
        }

        return categories;
    }

    public void addReview(String itemid, String review_text, String name, String stars) {
        Review review = new Review();
        review.setComment(review_text);
        review.setDate(new Date());
        review.setStars(getIntFromString(stars));
        review.setName(name);

        int itemdid_int = getIntFromString(itemid);

        Document pushUpdate = new Document( "$push", new Document("reviews", review));

        itemCollection.updateOne(eq("_id", itemdid_int), pushUpdate);
    }

    private int getIntFromString(String src) {
        if (src == null) {
            return 0;
        }

        return (new Integer(src));
    }
}
