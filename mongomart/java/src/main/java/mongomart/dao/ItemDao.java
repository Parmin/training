package mongomart.dao;

import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import mongomart.model.Item;

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
        return itemCollection.find(eq("_id", id)).first();
    }
}
