package mongomart.controller;

import com.mongodb.client.MongoDatabase;
import freemarker.template.Configuration;
import mongomart.config.FreeMarkerEngine;
import mongomart.config.Utils;
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

            ArrayList<Item> related_items = itemDao.getItems("0");

            HashMap<String, Object> attributes = new HashMap<String, Object>();
            attributes.put("item", item);
            attributes.put("itemid", itemid);
            attributes.put("related_items", related_items.subList(0, 4));

            // The hello.ftl file is located in directory:
            // src/test/resources/spark/template/freemarker
            return new ModelAndView(attributes, "item.ftl");
        }, new FreeMarkerEngine(cfg));

        get("/", (request, response) -> {
            String category = request.queryParams("category");
            String page = request.queryParams("page");

            ArrayList<Item> items = new ArrayList<Item>();
            ArrayList<Category> categories = itemDao.getCategoriesAndNumProducts();
            long itemCount = 0;

            // Search by category
            if (category != null && (!category.equals("All") && !category.trim().equals(""))) {
                items = itemDao.getItemsByCategory(category, page);
                itemCount = itemDao.getItemsByCategoryCount(category);
            }
            else {
                items = itemDao.getItems(page);
                itemCount = itemDao.getItemsCount();
                category = "All";
            }

            int num_pages = 0;
            if (itemCount > itemDao.getItemsPerPage()) {
                num_pages = (int)Math.ceil(itemCount / itemDao.getItemsPerPage());
            }

            HashMap<String, Object> attributes = new HashMap<String, Object>();
            attributes.put("items", items);
            attributes.put("item_count", itemCount);
            attributes.put("categories", categories);
            attributes.put("category_param", category);
            attributes.put("page", Utils.getIntFromString(page));
            attributes.put("num_pages", num_pages);

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


        get("/search", (request, response) -> {
            String query = request.queryParams("query");
            String page = request.queryParams("page");

            ArrayList<Item> items = itemDao.textSearch(query, page);
            long itemCount = itemDao.textSearchCount(query);

            int num_pages = 0;
            if (itemCount > itemDao.getItemsPerPage()) {
                num_pages = (int)Math.ceil(itemCount / itemDao.getItemsPerPage());
            }

            HashMap<String, Object> attributes = new HashMap<String, Object>();
            attributes.put("items", items);
            attributes.put("item_count", itemCount);
            attributes.put("query_string", query);
            attributes.put("page", Utils.getIntFromString(page));
            attributes.put("num_pages", num_pages);

            // The hello.ftl file is located in directory:
            // src/test/resources/spark/template/freemarker
            return new ModelAndView(attributes, "search.ftl");
        }, new FreeMarkerEngine(cfg));

    }
}
