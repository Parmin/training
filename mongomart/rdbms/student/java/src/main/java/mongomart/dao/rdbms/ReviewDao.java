package mongomart.dao.rdbms;


import mongomart.model.Review;

import java.util.ArrayList;
import java.util.List;
import java.sql.*;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

/**
 * All database access to the "review" collection
 */
public class ReviewDao {

    private final Connection connection;
    private Log log = LogFactory.getLog(ReviewDao.class);

    /**
     *
     * @param connection
     */
    public ReviewDao(final Connection connection) {
        this.connection = connection;
    }

    
    /** 
     * Returns the list of reviews for a given item
     * @param itemId
     * @return
     */
    public List<Review> getItemReviews(int itemId){
    	List<Review> reviews = new ArrayList<Review>();
    	String sqlQuery = "SELECT * FROM reviews WHERE items_id = ?";
    	
    	try {
    		PreparedStatement ps = this.connection.prepareStatement(sqlQuery);
            ps.setInt(1, itemId);
            ResultSet rs = ps.executeQuery();
            
            while(rs.next()){
            	reviews.add(this.resultSetToReview(rs));
            }
            
            rs.close();
            ps.close();
    	} catch (SQLException ex) {
    		log.error("Problem collecting reviews: " + ex.getMessage());
    	}
    	
    	return reviews;
    }
    


    /**
     * Get number of reviews for an item
     *
     * @param itemid itemid to calculate the number of reviews for
     * @return
     */
    public int numReviews(int itemid) {
        //return (int)reviewCollection.count(eq("itemid", itemid));
        String sqlQuery = "SELECT COUNT(*) as count FROM reviews WHERE items_id = ?";
        int numReviews = 0;

        try{

          PreparedStatement ps = this.connection.prepareStatement(sqlQuery);
          ps.setInt(1, itemid);
          ResultSet rs = ps.executeQuery();
          while(rs.next()){
        	  numReviews = rs.getInt("count");
          }

        } catch(SQLException ex){
          log.error("Refusing to run query: " + ex.getMessage());
        }

        return numReviews;
    }

    /**
     * Calculate the average number of stars per itemid
     *
     * @param itemid itemid to calculate average number of stars for
     */

    public int avgStars(int itemid) {
        double avg = 0.0;

        String sql = "SELECT AVG(stars) as avg FROM reviews WHERE items_id = ?";
        
        try{
            PreparedStatement ps = this.connection.prepareStatement(sql);
            ps.setInt(1, itemid);
            
            ResultSet rs = ps.executeQuery();
            while(rs.next()){
                avg = rs.getDouble("avg");
            }
            
            rs.close();
            ps.close();
        } catch (SQLException ex) {
            log.error("Issue calculating avg stars: " + ex.getMessage());
        }

        return (int)avg;
    }
    
    private Review resultSetToReview(ResultSet rs) throws SQLException{
    	Review rev = new Review();
    	
    	if(rs != null){
    		rev.setComment(rs.getString("comment"));
    		rev.setDate(rs.getDate("date"));
    		rev.setId(rs.getInt("id"));
    		rev.setName(rs.getString("name"));
    		rev.setItemid(rs.getInt("items_id"));
    		rev.setStars(rs.getInt("stars"));
    	}
    	
    	return rev;
    }
}
