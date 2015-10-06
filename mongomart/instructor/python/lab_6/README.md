Lab 6 Solution
==============

Please type in solution with the class instead of distributing source code.

This exercise gives basic practice using the $geoNear geospatial
operator. In the solution, the pipeline contruction has been factored
to a helper method (`build_closest_to_location_pipeline`), but it
could also inlined directly into `get_stores_closest_to_location`.


Modify storeDAO.py
------------------

- Update the `get_stores_closest_to_location` method:

```python
    def get_stores_closest_to_location(self, longitude, latitude, skip, limit):
        pipeline = self.build_closest_to_location_pipeline(longitude, latitude)
        pipeline.append({'$skip': skip})
        pipeline.append({'$limit': limit})
        return [self.doc_to_store(doc) for doc in self.store.aggregate(pipeline)]
```


- Add a `build_closest_to_location_pipeline` method:

```python
    def build_closest_to_location_pipeline(self, longitude, latitude):
        coordinates = [longitude, latitude]
        num_stores = self.count_stores()

        geo_near = {
            '$geoNear': {
                'near': {'type': 'Point',
                         'coordinates': coordinates},
                'distanceField': 'distance_from_point',
                'spherical': True,
                'distanceMultiplier': 0.001,
                'limit': num_stores
                }
        }
        return [geo_near]
```
