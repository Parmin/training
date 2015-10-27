class ZipNotFound(Exception):
    pass


class CityAndStateNotFound(Exception):
    pass


class StoreDAO(object):
    def __init__(self, database):
        self.db = database
        self.zip = self.db.zip
        self.store = self.db.store

    def get_all_states(self):
        return self.zip.distinct('state')

    def get_stores_closest_to_city_and_state(self, city, state, skip, limit):
        doc = self.zip.find_one({'city': city.toupper(), 'state': state})
        if doc is None:
            raise CityAndStateNotFound((city, state))
        location = doc['loc']
        return self.get_stores_closest_to_location(location[0], location[1], skip, limit)

    def get_stores_closest_to_zip(self, zip_code, skip, limit):
        doc = self.zip.find_one({'_id': zip_code})
        if doc is None:
            raise ZipNotFound(zip_code)
        loc = doc['loc']
        return self.get_stores_closest_to_location(loc[0], loc[1], skip, limit)

    def get_stores_closest_to_location(self, longitude, latitude, skip, limit):
        # TODO-lab6

        # Use the $geoNear aggregration operator to query for stores
        # in order of proximity to the specified point (i.e.,
        # longitude and latitude), skipping over `skip` documents and
        # limiting results to `limit`. Ensure that your document has
        # a computed field `distanceFromPoint` (see doc_to_store).

        docs = []

        # TODO-lab6 Replace code above.

        return [self.doc_to_store(doc) for doc in docs]

    def count_stores(self):
        return self.store.count()
        
    def doc_to_store(self, document):
        coords = document['coords'];
        longitude = coords[0]
        latitude = coords[1]

        distance_from_point = document.get('distance_from_point', 0.0)

        return {
            'id': document['_id'],
            'storeId': document['storeId'],
            'name': document['name'],
            'longitude': longitude,
            'latitude': latitude,
            'address': document['address'],
            'address2': document.get('address2'),
            'city': document['city'],
            'state': document['state'],
            'zip': document['zip'],
            'country': document['country'],
            'distance_from_point': distance_from_point
        }

