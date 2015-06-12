package mongomart.controller;

import com.mongodb.client.MongoDatabase;
import freemarker.template.Configuration;
import mongomart.config.FreeMarkerEngine;
import mongomart.dao.ItemDao;
import mongomart.model.Category;
import mongomart.model.Item;
import spark.ModelAndView;

import java.util.ArrayList;
import java.util.HashMap;

import static spark.Spark.get;

/**
 * Created by jason on 6/9/15.
 */
public class StoreController {

    public StoreController(Configuration cfg, MongoDatabase itemDatabase) {

        ItemDao itemDao = new ItemDao(itemDatabase);

        get("/item", (request, response) -> {
            String itemid = request.queryParams("id");

            Item item = itemDao.getItem(new Integer(itemid));

            /*
            Item item = new Item();
            item.populateDummyValues();
            */

            ArrayList<Item> related_items = new ArrayList<Item>();
            related_items.add(item);
            related_items.add(item);
            related_items.add(item);
            related_items.add(item);

            HashMap<String, Object> attributes = new HashMap<String, Object>();
            attributes.put("item", item);
            attributes.put("itemid", itemid);
            attributes.put("related_items", related_items);

            // The hello.ftl file is located in directory:
            // src/test/resources/spark/template/freemarker
            return new ModelAndView(attributes, "item.ftl");
        }, new FreeMarkerEngine(cfg));

        get("/", (request, response) -> {
            String category = request.queryParams("category");
            ArrayList<Item> items = new ArrayList<Item>();
            ArrayList<Category> categories = itemDao.getCategoriesAndNumProducts();

            // Search by category
            if (category != null && !category.trim().equals("")) {
                items = itemDao.getItemsByCategory(category);
            }
            else {
                items = itemDao.getItems();
                category = "All";
            }

            HashMap<String, Object> attributes = new HashMap<String, Object>();
            attributes.put("items", items);
            attributes.put("categories", categories);
            attributes.put("category_param", category);

            // The hello.ftl file is located in directory:
            // src/test/resources/spark/template/freemarker
            return new ModelAndView(attributes, "home.ftl");
        }, new FreeMarkerEngine(cfg));

        get("/add-review", (request, response) -> {
            String itemid = request.queryParams("itemid");
            String review = request.queryParams("review");
            String name = request.queryParams("name");
            String stars = request.queryParams("stars");

            itemDao.addReview(itemid, review, name, stars);

            response.redirect("/item?id=" + itemid);

            // spark hack, can never get to this point
            return null;
        }, new FreeMarkerEngine(cfg));

    }
}
