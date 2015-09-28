package mongomart.model;

import org.bson.types.ObjectId;

/**
 * Created by glowe on 6/19/15.
 */
public class Store {
    private final ObjectId id;
    private final String storeId;
    private final String name;
    private final double latitude;
    private final double longitude;
    private final String address;
    private final String address2;
    private final String city;
    private final String state;
    private final String zip;
    private final String country;
    private final double distanceFromPoint;

    public Store(final ObjectId id, final String storeId, final String name, final double longitude,
                 final double latitude, final String address, final String address2, final String city,
                 final String region, final String zip, final String country, final double distanceFromPoint) {
        this.id = id;
        this.storeId = storeId;
        this.name = name;
        this.longitude = longitude;
        this.latitude = latitude;
        this.address = address;
        this.address2 = address2;
        this.city = city;
        this.state = region;
        this.zip = zip;
        this.country = country;
        this.distanceFromPoint = distanceFromPoint;
    }

    public ObjectId getId() {
        return id;
    }

    public String getStoreId() {
        return storeId;
    }

    public String getName() {
        return name;
    }

    public double getLatitude() {
        return latitude;
    }

    public double getLongitude() {
        return longitude;
    }

    public String getAddress() {
        return address;
    }

    public String getAddress2() {
        return address2;
    }

    public String getCity() {
        return city;
    }

    public String getState() {
        return state;
    }

    public String getZip() {
        return zip;
    }

    public String getCountry() {
        return country;
    }

    public double getDistanceFromPoint() {
        return distanceFromPoint;
    }
}
