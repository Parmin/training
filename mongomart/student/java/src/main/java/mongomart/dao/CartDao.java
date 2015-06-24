package mongomart.dao;

import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import mongomart.model.Cart;
import mongomart.model.Item;
import org.bson.Document;

/**
 * All database access to the "cart" collection
 *
 * ALL T O D O BLOCKS MUST BE COMPLETED
 */
public class CartDao {
    // TODO-lab1 this variable must be assigned in constructor
    private final MongoCollection<Document> cartCollection;

    /**
     *
     * @param mongoMartDatabase
     */
    public CartDao(final MongoDatabase mongoMartDatabase) {

        /**
         * TODO-lab1
         *
         * LAB #1: Get the "cart" collection and assign it to cartCollection variable here
         *
         */
        cartCollection = null; // TODO-lab1 replace this line
    }

    /**
     * Get a cart by userid
     *
     * @param userid
     * @return
     */
    public Cart getCart(String userid) {

        /**
         * TODO-lab2
         *
         * LAB #2: Query the "cart" collection by userid and return a Cart object
         */

        Cart cart = Cart.getMockCart(); // TODO-lab2 replace this line

        return cart;
    }

    /**
     * Add an item to a cart
     *
     * @param item
     * @param userid
     */

    public void addToCart(Item item, String userid) {

        /**
         * TODO-lab2
         *
         * LAB #2: Add an item to a user's cart document
         *
         * HINT: There are several cases you must account for here, such as an empty initial cart
         */

    }

    /**
     * Update the quantity of an item in a cart.  If quantity is 0, remove item from cart
     *
     * @param itemid
     * @param quantity
     * @param userid
     */
    public void updateQuantity(int itemid, int quantity, String userid) {

        /**
         * TODO-lab2
         *
         * LAB #2: Update the quantity of an item in a users cart, if the quantity is 0, remove the item from the cart
         *
         * HINT: You may want to create a helper method for determining if an item already exists in a cart
         */

    }

}
