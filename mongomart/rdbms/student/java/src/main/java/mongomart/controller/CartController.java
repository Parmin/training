package mongomart.controller;

import static spark.Spark.get;

import java.sql.Connection;
import java.util.HashMap;

import mongomart.config.FreeMarkerEngine;
import mongomart.config.Utils;
import mongomart.dao.rdbms.CartDao;
import mongomart.dao.rdbms.ItemDao;
import mongomart.model.Cart;
import mongomart.model.Item;
import spark.ModelAndView;
import freemarker.template.Configuration;

/**
 * MongoMart shopping cart controller
 *
 * Provide functionality to:
 *      - Add items to a cart
 *      - Remove items from a cart
 *      - Update quantities in a cart
 */
public class CartController {
    // Hardcoded userid, only one user currently allowed in the system
    public final String USERID = "558098a65133816958968d88";

    /**
     * Create cart routes
     *
     * @param cfg
     * @param connection
     */
    public CartController(Configuration cfg, Connection connection) {

        CartDao cartDao = new CartDao(connection);
        ItemDao itemDao = new ItemDao(connection);

        // View cart
        get("/cart", (request, response) -> {
            Cart cart = cartDao.getCart(USERID);

            HashMap<String, Object> attributes = new HashMap<>();
            attributes.put("cart", cart);
            attributes.put("total", calculateCartTotal(cart));

            return new ModelAndView(attributes, "cart.ftl");
        }, new FreeMarkerEngine(cfg));

        // Update quantities in a cart
        // Specifying a quantity of 0 means remove items from the cart
        get("/cart/update", (request, response) -> {
            String itemid = request.queryParams("itemid");
            String quantity = request.queryParams("quantity");

            cartDao.updateQuantity(Utils.getIntFromString(itemid), Utils.getIntFromString(quantity), USERID);
            Cart cart = cartDao.getCart(USERID);

            HashMap<String, Object> attributes = new HashMap<>();
            attributes.put("cart", cart);
            attributes.put("updated", true);
            attributes.put("total", calculateCartTotal(cart));
            return new ModelAndView(attributes, "cart.ftl");
        }, new FreeMarkerEngine(cfg));

        // Add a new item to the user's cart
        get("/cart/add", (request, response) -> {
            // itemid to add
            String itemid = request.queryParams("itemid");
            // Lookup item information, to add title, img_url, etc. to cart
            Item item = itemDao.getItem(Utils.getIntFromString(itemid));
            item.setQuantity(1);
            cartDao.addToCart(item, USERID);

            Cart cart = cartDao.getCart(USERID);

            HashMap<String, Object> attributes = new HashMap<>();
            attributes.put("cart", cart);
            attributes.put("updated", true);
            attributes.put("total", calculateCartTotal(cart));

            return new ModelAndView(attributes, "cart.ftl");
        }, new FreeMarkerEngine(cfg));


    }

    /**
     * Helper method to calculate a cart's total
     *
     * @param cart
     * @return
     */
    private double calculateCartTotal(Cart cart) {
        double total = 0.0;
        for (Item item : cart.getItems()) {
            total += (item.getPrice() * item.getQuantity());
        }
        return total;
    }
}
