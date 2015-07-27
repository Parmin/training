Lab 5 Solution
==============

Please type in solution with the class instead of distributing source code.

This exercise is hard.  There are multiple ways to convert the existing application to use range based pagination.  One method is described below.

This solution omits using the "category" parameter (no query will use this field).

Modify mongomart.py (only for get("/") )
----------------------------------------

- Set useRangeBasedPagination = True
- Use befor/after parameters

```
# for range based pagination
before = request.query.before or 0
after = request.query.after or 0
```

- Call a method in itemDao with the before/after parameters: all_items = items.get_items_range_based(int(before), int(after), ITEMS_PER_PAGE)
- Set the correct number of items to return (since we always get items per page + 1, to determine if there is a previous/next page needed)

```
if num_items > ITEMS_PER_PAGE:
        # Since we got back one extra item than we needed, we need to trim it
        if before > 0:
            all_items = all_items[1:len(all_items)];
        else:
            all_items = all_items[0:ITEMS_PER_PAGE];
```

- Set the URLs for next/previous pages:

```
if include_next_page(num_items, before, after):
        next_page_url = '/?after=' + str(all_items[len(all_items)-1]['_id'])

    if include_previous_page(num_items, before, after):
        previous_page_url = '/?before=' + str(all_items[0]['_id'])
```

Create a new method in itemDao get_items_range_based(self, before, after, items_per_page)
-----------------------------------------------------------------------------------------

- Query based on a range
- Sort direction and query operator ($lt vs $gt) based on before/after parameter (reddit.com uses the same algorithm for pagination)
- Look at pagination on reddit.com to see a similar method

```
def get_items_range_based(self, before, after, items_per_page):

    if before > 0:
        items = list(self.item.find( { '_id' : { '$lt' : before }}).sort( '_id' , pymongo.DESCENDING).limit(items_per_page + 1))

        #reverse order of results
        items.reverse()
    else:
        items = list(self.item.find( { '_id' : { '$gt' : after }}).sort( '_id' , pymongo.ASCENDING).limit(items_per_page + 1))

    return items
```



