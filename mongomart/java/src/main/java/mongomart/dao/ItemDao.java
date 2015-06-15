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
import java.util.Date;
import java.util.List;

import static com.mongodb.client.model.Filters.eq;

/**
 * Created by jason on 6/9/15.
 */
public class ItemDao {
    private static final int ITEMS_PER_PAGE = 5;

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

    public ArrayList<Item> getItems(String page_str) {
        ArrayList<Item> items = new ArrayList<>();
        int page = Utils.getIntFromString(page_str);

        MongoCursor<Item> cursor = itemCollection.find()
                                                 .skip(ITEMS_PER_PAGE * page)
                                                 .limit(ITEMS_PER_PAGE)
                                                 .iterator();
        while (cursor.hasNext()) {
            items.add(cursor.next());
        }

        return items;
    }

    public long getItemsCount() {
        return itemCollection.count();
    }

    public ArrayList<Item> getItemsByCategory(String category, String page_str) {
        ArrayList<Item> items = new ArrayList<>();
        int page = Utils.getIntFromString(page_str);

        MongoCursor<Item> cursor = itemCollection.find(eq("category", category))
                                                 .skip(ITEMS_PER_PAGE * page)
                                                 .limit(ITEMS_PER_PAGE)
                                                 .iterator();
        while (cursor.hasNext()) {
            items.add(cursor.next());
        }

        return items;
    }

    public long getItemsByCategoryCount(String category) {
        return itemCollection.count(eq("category", category));
    }

    public ArrayList<Category> getCategoriesAndNumProducts() {
        ArrayList<Category> categories = new ArrayList<>();

        // db.item.aggregate( { $group : { "_id" : "$category", "num" : { "$sum" : 1 } } }, { $sort : { "_id" : 1 } })
        Document groupStage = new Document("$group",
                (new Document( "_id", "$category")).append("num", new Document("$sum", 1)));
        Document sortStage = new Document("$sort", new Document("_id", 1));

        List<Document> aggregateStages = new ArrayList<Document>();
        aggregateStages.add(groupStage);
        aggregateStages.add(sortStage);

        MongoCursor<Document> cursor = itemCollection.aggregate(aggregateStages, Document.class).useCursor(true).iterator();

        int total_count = 0;
        while (cursor.hasNext()) {
            Document resultDoc = cursor.next();
            Category category = new Category(resultDoc.getString("_id"), resultDoc.getInteger("num"));
            System.out.println("Category: " + resultDoc.getString("_id") + ", num:" + resultDoc.getInteger("num"));
            categories.add(category);
            total_count += resultDoc.getInteger("num");
        }

        categories.add(0, new Category("All", total_count));

        return categories;
    }

    public void addReview(String itemid, String review_text, String name, String stars) {
        Review review = new Review();
        review.setComment(review_text);
        review.setDate(new Date());
        review.setStars(Utils.getIntFromString(stars));
        review.setName(name);

        int itemdid_int = Utils.getIntFromString(itemid);

        Document pushUpdate = new Document( "$push", new Document("reviews", review));

        itemCollection.updateOne(eq("_id", itemdid_int), pushUpdate);
    }

    public int getItemsPerPage() {
        return ITEMS_PER_PAGE;
    }
}
