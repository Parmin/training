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
import java.util.List;

import static mongomart.config.Utils.isEmpty;
import static spark.Spark.get;

/**
 * MongoMart store/item controller
 *
 * Provide functionality to:
 *      - View an item
 *      - View items in a category
 *      - Add a review
 *      - Text search for items
 */
public class StoreController {

    /**
     *
     * @param cfg
     * @param itemDatabase
     */
    public StoreController(Configuration cfg, MongoDatabase itemDatabase) {

        ItemDao itemDao = new ItemDao(itemDatabase);

        // Homepage and category search
        get("/", (request, response) -> {
            String category = request.queryParams("category");
            String page = request.queryParams("page");

            /**
             * lab3
             *
             * LAB #3: Add before/after parameters for range based pagination
             *
             */

            // Set to true for lab 3
            boolean useRangeBasedPagination = true;

            String before = request.queryParams("before");
            String after = request.queryParams("after");


            List<Item> items = new ArrayList<>();
            ArrayList<Category> categories = itemDao.getCategoriesAndNumProducts();
            long itemCount = 0;

            // Search by category
            if (category != null && (!category.equals("All") && !category.trim().equals(""))) {
                items = itemDao.getItemsByCategory(category, page);
                itemCount = itemDao.getItemsByCategoryCount(category);
            }
            // Else show all items
            else {
                /**
                 * lab3
                 *
                 * LAB #3: Create new method in ItemDao to use before/after parameters
                 *
                 */
                items = itemDao.getItemsRangeBased(before, after);

                category = "All";
            }

            // Determine the number of pages to display in the UI (pagination)
            int num_pages = 0;
            if (itemCount > itemDao.getItemsPerPage()) {
                num_pages = (int)Math.ceil(itemCount / itemDao.getItemsPerPage());
            }

            HashMap<String, Object> attributes = new HashMap<>();

            /**
             * lab3
             *
             * LAB #3: Since we bring back one extra item than is needed (to determine if there is a
             * next/previous page), we need to trim the result set back to itemDao.getItemsPerPage()
             *
             */
            int num_items = items.size();
            if (items != null && items.size() > itemDao.getItemsPerPage()) {

                // Since we got back one extra item than we needed, we need to trim it
                if (items.size() > itemDao.getItemsPerPage()) {
                    if (before != null) {
                        items = items.subList(1, items.size());
                    } else {
                        items = items.subList(0, itemDao.getItemsPerPage());
                    }
                }
            }

            /**
             * TODO-lab3
             *
             * LAB #3: The nextPageUrl and previousPageUrl attributes are used by home.ftl for displaying previous and
             * next page.  If either is null, previous/next page will not be displayed
             *
             * HINT: make sure to only set nextPageUrl or previousPageUrl when you want them to be displayed in the UI
             *
             */
            if (useRangeBasedPagination) {
                if (includeNextPage(num_items, before, after, itemDao.getItemsPerPage())) {
                    attributes.put("nextPageUrl", "/?after=" + items.get(items.size()-1).getId());
                }
                if (includePreviousPage(num_items, before, after, itemDao.getItemsPerPage())) {
                    attributes.put("previousPageUrl", "/?before=" + items.get(0).getId());
                }
            }

            attributes.put("useRangeBasedPagination", useRangeBasedPagination);
            attributes.put("items", items);
            attributes.put("categories", categories);
            attributes.put("category_param", category);
            attributes.put("page", Utils.getIntFromString(page));
            attributes.put("num_pages", num_pages);

            return new ModelAndView(attributes, "home.ftl");
        }, new FreeMarkerEngine(cfg));

        // View an item
        get("/item", (request, response) -> {
            String itemid = request.queryParams("id");
            HashMap<String, Object> attributes = buildItemResponse(itemid, itemDao);
            return new ModelAndView(attributes, "item.ftl");
        }, new FreeMarkerEngine(cfg));

        // Add a review for an item
        get("/add-review", (request, response) -> {
            String itemid = request.queryParams("itemid");
            String review = request.queryParams("review");
            String name = request.queryParams("name");
            String stars = request.queryParams("stars");

            itemDao.addReview(itemid, review, name, stars);

            HashMap<String, Object> attributes = buildItemResponse(itemid, itemDao);
            return new ModelAndView(attributes, "item.ftl");
        }, new FreeMarkerEngine(cfg));

        // Text search for an item, requires a text index
        get("/search", (request, response) -> {
            String query = request.queryParams("query");
            String page = request.queryParams("page");

            List<Item> items = itemDao.textSearch(query, page);
            long itemCount = itemDao.textSearchCount(query);

            // Determine the number of pages to display in the UI (pagination)
            int num_pages = 0;
            if (itemCount > itemDao.getItemsPerPage()) {
                num_pages = (int)Math.ceil(itemCount / itemDao.getItemsPerPage());
            }

            HashMap<String, Object> attributes = new HashMap<>();
            attributes.put("items", items);
            attributes.put("item_count", itemCount);
            attributes.put("query_string", query);
            attributes.put("page", Utils.getIntFromString(page));
            attributes.put("num_pages", num_pages);

            return new ModelAndView(attributes, "search.ftl");
        }, new FreeMarkerEngine(cfg));

    }

    /**
     * Construct the necessary UI attributes to render an Item page
     *
     * @param itemid
     * @param itemDao
     * @return
     */
    private HashMap<String, Object> buildItemResponse(String itemid, ItemDao itemDao) {
        List<Item> related_items = itemDao.getItems("0");
        Item item = itemDao.getItem(new Integer(itemid));

        HashMap<String, Object> attributes = new HashMap<>();
        attributes.put("item", item);
        attributes.put("itemid", itemid);
        attributes.put("related_items", related_items.subList(0, 4));
        return attributes;
    }

    private boolean includeNextPage(int num_items, String before, String after, int items_per_page) {

        // If homepage, display a next link is number of items is large enough
        if (isEmpty(before) && isEmpty(after) && num_items > items_per_page) {
                return true;
        }

        // If only a "before" parameter is passed in
        else if (!isEmpty(before)) {
            return true;
        }

        // Only an "after" parameter was passed in
        else if (num_items > items_per_page) {
            return true;
        }

        return false;
    }

    private boolean includePreviousPage(int num_items, String before, String after, int items_per_page) {

        if (!isEmpty(after)) {
            return true;
        }
        // If only a "before" parameter is passed in
        else if (!isEmpty(before) && num_items > items_per_page) {
            return true;
        }

        return false;
    }
}
