package mongomart.dao.rdbms;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;
import java.util.SortedSet;
import java.util.TreeSet;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

import mongomart.model.Address;
import mongomart.model.Geo;
import mongomart.model.Store;

public class StoreDao {

    Connection connection;

    private Log log = LogFactory.getLog(StoreDao.class);

    public static class ZipNotFound extends Exception {
        /**
         *
         */
        private static final long serialVersionUID = 1342132413421242369L;
        public final String zip;

        public ZipNotFound(final String zip) {
            super();
            this.zip = zip;
        }
    }


    public StoreDao(final Connection connection){
        this.connection = connection;
    }


    public long countStores() {
        String sql = "SELECT COUNT(1) as count FROM stores";
        long count = 0L;
        try {
            PreparedStatement ps = connection.prepareStatement(sql);
            ResultSet rs = ps.executeQuery();

            while(rs.next()){
                count = rs.getLong("count");
                break;
            }

            rs.close();
            ps.close();
        } catch(SQLException ex){
            log.error("Issue counting stores: " + ex.getMessage());
        }
        return count;
    }

    private List<Store> getStoreByZip(String zip) throws SQLException, ZipNotFound{
        List<Store> stores = new ArrayList<Store>();
        String sql = "SELECT * FROM stores s, addresses a, geo g " +
            "WHERE a.id = s.address_id AND g.id = s.geo_id AND a.zip = ?";

        PreparedStatement ps = connection.prepareStatement(sql);
        ps.setString(1, zip);
        ResultSet rs = ps.executeQuery();

        while (rs.next()) {
            String storeId = rs.getString("store_id");
            String name = rs.getString("name");
            Geo geo = new Geo(rs.getDouble("longitude"), rs.getDouble("latitude"));
            Address address = new Address(rs.getString("line1"), rs.getString("line2"),
                rs.getString("city"), rs.getString("state"), rs.getString("zip"), rs.getString("country"));

            double distanceFromPoint = 0;

            stores.add(new Store(null, storeId, name, geo, address, distanceFromPoint));
        }

        ps.close();
        rs.close();

        if (stores.size() < 1){
            throw new ZipNotFound(zip);
        }

        return stores;

    }

    public List<Store> getStoresClosestToZip(String zipCode, int skip, int limit) throws ZipNotFound {
        List<Store> stores = new ArrayList<Store>();
        try{
            stores = getStoreByZip(zipCode);
        } catch(SQLException ex) {
            log.error("Issue with getting all states: " + ex.getMessage());
        }
        return stores;
    }


    public SortedSet<String> getAllStates() {
        String sqlSelect = "SELECT DISTINCT(state) as state FROM addresses";
        SortedSet<String> states = new TreeSet<String>();
        try {
            PreparedStatement ps = connection.prepareStatement(sqlSelect);
            ResultSet rs = ps.executeQuery();

            while(rs.next()){
                states.add(rs.getString("state"));
            }


            rs.close();
            ps.close();
        } catch(SQLException ex){
            log.error("Issue with getting all states: " + ex.getMessage());
        }
        return states;
    }



}
