package mongomart.controller;

import com.mongodb.client.MongoDatabase;
import freemarker.template.Configuration;
import mongomart.config.FreeMarkerEngine;
import mongomart.dao.ItemDao;
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
            Item item = itemDao.getItem(1);

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
            attributes.put("related_items", related_items);

            // The hello.ftl file is located in directory:
            // src/test/resources/spark/template/freemarker
            return new ModelAndView(attributes, "item.ftl");
        }, new FreeMarkerEngine(cfg));

    }
}
