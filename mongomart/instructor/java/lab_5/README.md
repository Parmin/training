Lab 5 Solution
==============

This exercise is hard.  There are multiple ways to convert the existing application to use range based pagination.  One method is described below.

Modify StoreController.java (only for get("/") )
------------------------------------------------

- Set useRangeBasedPagination = true
- Use befor/after parameters

```
String before = request.queryParams("before");
String after = request.queryParams("after");
```

- Call a method in ItemDao with the before/after parameters: items = itemDao.getItemsRangeBased(before, after);
- Set the correct number of items to return (since we always get items per page + 1, to determine if there is a previous/next page needed)

```
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
```

- Set the URLs for next/previous pages:

```
if (useRangeBasedPagination) {
    if (includeNextPage(num_items, before, after, itemDao.getItemsPerPage())) {
        attributes.put("nextPageUrl", "/?after=" + items.get(items.size()-1).getId());
    }
    if (includePreviousPage(num_items, before, after, itemDao.getItemsPerPage())) {
        attributes.put("previousPageUrl", "/?before=" + items.get(0).getId());
    }
}
```

Create a new method in ItemDao.java getItemsRangeBased(String before, String after)
-----------------------------------------------------------------------------------

- Query based on a range
- Sort direction and query operator ($lt vs $gt) based on before/after parameter (reddit.com uses the same algorithm for pagination)
- Look at pagination on reddit.com to see a similar method



