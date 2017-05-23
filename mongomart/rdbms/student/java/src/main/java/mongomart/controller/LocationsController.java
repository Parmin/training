package mongomart.controller;

import static mongomart.config.Utils.getIntFromString;
import static mongomart.config.Utils.isEmpty;
import static spark.Spark.get;

import java.sql.Connection;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.SortedSet;

import mongomart.config.FreeMarkerEngine;
import mongomart.dao.rdbms.StoreDao;
import mongomart.model.Store;
import spark.ModelAndView;
import freemarker.template.Configuration;

/**
 * Created by gl on 7/16/15.
 */
public class LocationsController {


    /**
     *
     * @param cfg
     * @param storeDatabase
     */
    public LocationsController(Configuration cfg, Connection connection) {
        
        StoreDao storeDao = new StoreDao(connection);

        get("/locations", (request, response) -> {
            String city = request.queryParams("city");
            String state = request.queryParams("state");
            String zip = request.queryParams("zip");
            String find = request.queryParams("find");

            // Pagination calculations
            int page = getIntFromString(request.queryParams("page"));
            int storesPerPage = 5;
            int skip = storesPerPage * page;
            long numStores = storeDao.countStores();
            int numPages = ((int) Math.ceil(numStores / (double) storesPerPage));

            Map<String, Object> attributes = new HashMap<>();

            List<Store> stores = new ArrayList<>();
            if ("byZip".equals(find)) {
                if (isEmpty(zip)) {
                    attributes.put("zipError", "Please supply a zip.");
                } else {
                    zip = zip.trim();
                    try {
                        stores = storeDao.getStoresClosestToZip(zip, skip, storesPerPage);
                    } catch (StoreDao.ZipNotFound e) {
                        attributes.put("zipError", "Can't find " + zip + " in our database.");
                    }
                }
                city = "";
                state = "";
            } 
            SortedSet<String> states = storeDao.getAllStates();
            attributes.put("stores", stores);
            attributes.put("numStores", numStores);
            attributes.put("find", find);
            attributes.put("states", states);
            attributes.put("city", city);
            attributes.put("state", state);
            attributes.put("zip", zip);
            attributes.put("page", page);
            attributes.put("numPages", numPages);
            return new ModelAndView(attributes, "locations.ftl");
        }, new FreeMarkerEngine(cfg));
    }
}
