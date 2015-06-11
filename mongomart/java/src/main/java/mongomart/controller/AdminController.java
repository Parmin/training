package mongomart.controller;

import com.mongodb.client.MongoDatabase;
import freemarker.template.Configuration;
import mongomart.config.FreeMarkerEngine;
import spark.ModelAndView;

import java.util.HashMap;
import java.util.Map;

import static spark.Spark.get;

/**
 * Created by jason on 6/9/15.
 */
public class AdminController {
    private Configuration configuration;

    public AdminController(Configuration cfg, MongoDatabase itemDatabase) {

        get("/hello", (request, response) -> {
            Map<String, Object> attributes = new HashMap<>();
            attributes.put("message", "Hello World!");

            // The hello.ftl file is located in directory:
            // src/test/resources/spark/template/freemarker
            return new ModelAndView(attributes, "item.ftl");
        }, new FreeMarkerEngine(cfg));

    }
}
