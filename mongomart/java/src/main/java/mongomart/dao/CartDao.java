package mongomart.dao;

import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import com.mongodb.client.model.UpdateOptions;
import mongomart.model.Cart;
import mongomart.model.Item;
import org.bson.Document;

import java.util.ArrayList;
import java.util.List;

import static com.mongodb.client.model.Filters.and;
import static com.mongodb.client.model.Filters.eq;

/**
 * All database access to the "cart" collection
 */
public class CartDao {
    private final MongoCollection<Document> cartCollection;

    /**
     *
     * @param mongoMartDatabase
     */
    public CartDao(final MongoDatabase mongoMartDatabase) {
        cartCollection = mongoMartDatabase.getCollection("cart");
    }

    /**
     * Get a cart by userid
     *
     * @param userid
     * @return
     */
    public Cart getCart(String userid) {
        return docToCart(cartCollection.find(eq("userid", userid)).first());
    }

    /**
     * Add an item to a cart
     *
     * @param item
     * @param userid
     */

    public void addToCart(Item item, String userid) {
        if (existsInCart(item.getId(), userid)) {
            // increment amount in cart by 1
            // db.cart.update({ "userid" : "558098a65133816958968d88", "items._id": 3 }, { $inc : { "items.$.quantity" : 1 } } )
            cartCollection.updateOne(and(eq("userid", userid), eq("items._id", item.getId())),
                                     new Document("$inc", new Document("items.$.quantity", 1)));
        }
        else {
            // add item to cart or update quantity
            Document push = new Document("$push",
                    new Document("items", new Document("_id", item.getId())
                                          .append("title", item.getTitle())
                                          .append("category", item.getCategory())
                                          .append("price", item.getPrice())
                                          .append("quantity", item.getQuantity())
                                          .append("img_url", item.getImg_url())));

            cartCollection.updateOne(eq("userid", userid), push, new UpdateOptions().upsert(true));
        }

    }

    /**
     * Update the quantity of an item in a cart.  If quantity is 0, remove item from cart
     *
     * @param itemid
     * @param quantity
     * @param userid
     */
    public void updateQuantity(int itemid, int quantity, String userid) {
        if (quantity > 0) {
            // db.cart.update( { "userid" : "558098a65133816958968d88", "items._id" : 3 }, { $set : { "items.$.quantity" : 5} } )
            cartCollection.updateOne(and(eq("userid", userid),eq("items._id", itemid)),
                    new Document("$set", new Document( "items.$.quantity", quantity)));

        }
        else {
            // db.cart.update({ "userid" : "558098a65133816958968d88"}, { $pull : { "items" : { "_id" : 1 } } } )
            cartCollection.updateOne(eq("userid", userid),
                                     new Document("$pull", new Document( "items", new Document( "_id", itemid ))));
        }
    }

    /**
     * Determine if an item is already in a cart, useful for when "Add to cart" has been clicked for an existing item
     * in the user's cart, then the quantity just be incremented by 1
     *
     * @param itemid
     * @param userid
     * @return
     */
    public boolean existsInCart(int itemid, String userid) {
        long found = cartCollection.count(and(eq("userid", userid),eq("items._id", itemid)));
        return found > 0;
    }

    private Cart docToCart(Document document) {
        Cart cart = new Cart();
        cart.setId(document.getObjectId("_id"));
        cart.setStatus(document.getString("status"));
        cart.setLast_modified(document.getDate("last_modified"));
        cart.setUserid(document.getString("userid"));
        if (document.containsKey("items") && document.get("items") instanceof List) {
            List<Item> items = new ArrayList<>();
            List<Document> itemsList = (List<Document>)document.get("items");

            for (Document itemDoc : itemsList) {
                Item item = new Item();

                if (itemDoc.containsKey("_id")) {
                    item.setId(itemDoc.getInteger("_id"));
                }

                if (itemDoc.containsKey("quantity")) {
                    item.setQuantity(itemDoc.getInteger("quantity"));
                }

                if (itemDoc.containsKey("title")) {
                    item.setTitle(itemDoc.getString("title"));
                }

                if (itemDoc.containsKey("img_url")) {
                    item.setImg_url(itemDoc.getString("img_url"));
                }

                if (itemDoc.containsKey("price")) {
                    item.setPrice(itemDoc.getDouble("price"));
                }

                items.add(item);
            }

            cart.setItems(items);
        }
        else {
            cart.setItems(new ArrayList<>());
        }

        return cart;
    }
}
