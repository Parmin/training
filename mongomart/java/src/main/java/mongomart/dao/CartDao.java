package mongomart.dao;

import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import com.mongodb.client.model.UpdateOptions;
import mongomart.model.Cart;
import mongomart.model.Item;
import org.bson.Document;

import static com.mongodb.client.model.Filters.eq;

/**
 * Created by jason on 6/15/15.
 */
public class CartDao {
    private final MongoCollection<Cart> cartCollection;

    public CartDao(final MongoDatabase mongoMartDatabase) {
        cartCollection = mongoMartDatabase.getCollection("cart", Cart.class);
    }

    public Cart getCart(String userid) {
        return cartCollection.find(eq("userid", userid)).first();
    }

    public void addToCart(Item item, String userid) {
        item.optimizeForCart();

        if (existsInCart(item.getId(), userid)) {
            // increment amount in cart by 1
            // db.cart.update({ "userid" : "558098a65133816958968d88", "items._id": 3 }, { $inc : { "items.$.quantity" : 1 } } )
            cartCollection.updateOne(new Document("userid", userid).append("items._id", item.getId()),
                                     new Document("$inc", new Document( "items.$.quantity", 1)));
        }
        else {
            // add item to cart or update quantity
            Document push = new Document("$push", new Document("items", item));
            cartCollection.updateOne(new Document("userid", userid), push, new UpdateOptions().upsert(true));
        }

    }

    public void updateQuantity(int itemid, int quantity, String userid) {
        if (quantity > 0) {
            cartCollection.updateOne(new Document("userid", userid).append("items._id", itemid),
                    new Document("$set", new Document( "items.$.quantity", quantity)));

        }
        else {
            // db.cart.update({ "userid" : "558098a65133816958968d88"}, { $pull : { "items" : { "_id" : 1 } } } )
            cartCollection.updateOne(new Document("userid", userid),
                                     new Document("$pull", new Document( "items", new Document( "_id", itemid ))));
        }


    }

    public boolean existsInCart(int itemid, String userid) {
        long found = cartCollection.count(new Document("userid", userid).append("items._id", itemid));
        return found > 0;
    }
}
