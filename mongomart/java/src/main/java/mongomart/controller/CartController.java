package mongomart.controller;

import com.mongodb.client.MongoDatabase;
import freemarker.template.Configuration;
import mongomart.config.FreeMarkerEngine;
import mongomart.config.Utils;
import mongomart.dao.CartDao;
import mongomart.dao.ItemDao;
import mongomart.model.Cart;
import mongomart.model.Item;
import spark.ModelAndView;

import java.util.HashMap;

import static spark.Spark.get;

/**
 * Created by jason on 6/15/15.
 */
public class CartController {
    public final String USERID = "558098a65133816958968d88"; // hardcoded userid

    public CartController(Configuration cfg, MongoDatabase mongoMartDatabase) {

        CartDao cartDao = new CartDao(mongoMartDatabase);
        ItemDao itemDao = new ItemDao(mongoMartDatabase);

        get("/cart", (request, response) -> {
            Cart cart = cartDao.getCart(USERID);

            HashMap<String, Object> attributes = new HashMap<String, Object>();
            attributes.put("cart", cart);
            attributes.put("total", calculateCartTotal(cart));

            return new ModelAndView(attributes, "cart.ftl");
        }, new FreeMarkerEngine(cfg));

        get("/cart/update", (request, response) -> {
            String itemid = request.queryParams("itemid");
            String quantity = request.queryParams("quantity");

            cartDao.updateQuantity(Utils.getIntFromString(itemid), Utils.getIntFromString(quantity), USERID);
            Cart cart = cartDao.getCart(USERID);

            // update cart here
            HashMap<String, Object> attributes = new HashMap<String, Object>();
            attributes.put("cart", cart);
            attributes.put("updated", true);
            attributes.put("total", calculateCartTotal(cart));
            return new ModelAndView(attributes, "cart.ftl");
        }, new FreeMarkerEngine(cfg));

        get("/cart/add", (request, response) -> {
            String itemid = request.queryParams("itemid");
            Item item = itemDao.getItem(Utils.getIntFromString(itemid));
            item.setQuantity(1);
            cartDao.addToCart(item, USERID);

            Cart cart = cartDao.getCart(USERID);

            HashMap<String, Object> attributes = new HashMap<String, Object>();
            attributes.put("cart", cart);
            attributes.put("updated", true);
            attributes.put("total", calculateCartTotal(cart));

            // The hello.ftl file is located in directory:
            // src/test/resources/spark/template/freemarker
            return new ModelAndView(attributes, "cart.ftl");
        }, new FreeMarkerEngine(cfg));

    }

    private double calculateCartTotal(Cart cart) {
        double total = 0.0;
        for (Item item : cart.getItems()) {
            total += (item.getPrice() * item.getQuantity());
        }
        return total;
    }
}
