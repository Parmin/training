package mongomart.model;

import org.bson.types.ObjectId;

import java.util.List;

/**
 * Created by glowe on 6/19/15.
 */
public class Store {
    public final ObjectId _id;
    public final String storeId;
    public final String name;
    public final double latitude;
    public final double longitude;
    public final String address;
    public final String address2;
    public final String city;
    public final String state;
    public final String zip;
    public final String country;

    public Store(final ObjectId id, final String storeId, final String name, final double longitude,
                 final double latitude, final String address, final String address2, final String city,
                 final String state, final String zip, final String country) {
        this._id = id;
        this.storeId = storeId;
        this.name = name;
        this.longitude = longitude;
        this.latitude = latitude;
        this.address = address;
        this.address2 = address2;
        this.city = city;
        this.state = state;
        this.zip = zip;
        this.country = country;
    }
}
