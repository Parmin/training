package mongomart.controller;

import com.mongodb.client.MongoDatabase;
import freemarker.template.Configuration;
import mongomart.config.FreeMarkerEngine;
import mongomart.dao.StoreDao;
import mongomart.model.Store;
import spark.ModelAndView;

import java.util.HashMap;
import java.util.List;
import java.util.SortedSet;

import static spark.Spark.get;


/**
 * Created by gl on 7/16/15.
 */
public class LocationsController {


    /**
     *
     * @param cfg
     * @param storeDatabase
     */
    public LocationsController(Configuration cfg, MongoDatabase storeDatabase) {

        StoreDao storeDao = new StoreDao(storeDatabase);

        get("/locations", (request, response) -> {
            String query = request.queryParams("query");
            String zipCode = request.queryParams("zipCode");
            HashMap<String, Object> attributes = new HashMap<>();
            List<Store> stores = storeDao.getStoresClosestToZip(zipCode);
            long numStores = 10;
            SortedSet<String> states = storeDao.getAllStates();
            attributes.put("stores", stores);
            attributes.put("numStores", numStores);
            attributes.put("query", query);
            attributes.put("states", states);
            return new ModelAndView(attributes, "locations.ftl");
        }, new FreeMarkerEngine(cfg));
    }
}
