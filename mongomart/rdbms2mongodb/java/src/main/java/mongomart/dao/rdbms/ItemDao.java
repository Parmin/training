package mongomart.dao.rdbms;


import java.sql.Connection;
import java.sql.Date;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

import mongomart.config.Utils;
import mongomart.model.Category;
import mongomart.model.Item;
import mongomart.model.Review;

/**
 * All database access to the "item" collection
 */
public class ItemDao {
    private Log log = LogFactory.getLog(ItemDao.class);
	// Used for pagination
	private static final int ITEMS_PER_PAGE = 5;

	private final Connection connection;

	/**
	 *
	 * @param connection
	 */
	public ItemDao(final Connection connection) {
		this.connection = connection;
	}

	/**
	 * Get an Item by id
	 *
	 * @param id
	 * @return
	 */
	public Item getItem(int id) {
		String sqlQuery = "SELECT * FROM items i WHERE i.id = ?";
		Item it = new Item();
		try{
			PreparedStatement ps = this.connection.prepareStatement(sqlQuery);
			ps.setInt(1, id);
			ResultSet rs = ps.executeQuery();

			while(rs.next()){
				it = this.resultSetToItem(rs);
				break;
			}

			rs.close();
		} catch (SQLException ex){
			log.error("Like POTUS would say -> WRONG: " + ex.getMessage());
		}

		return it;

	}


	/**
	 * Get items by page number
	 *
	 * @param page_str
	 * @return
	 */
	public List<Item> getItems(String page_str) {
		String sqlQuery = "SELECT * FROM items LIMIT ? OFFSET ?";
		List<Item> list = new ArrayList<Item>();
		int page = Utils.getIntFromString(page_str);

		try{
			PreparedStatement ps = this.connection.prepareStatement(sqlQuery);
			ps.setInt(1, ITEMS_PER_PAGE);
			ps.setInt(2, ITEMS_PER_PAGE * page);
			ResultSet rs = ps.executeQuery();

			while(rs.next()){

				list.add(resultSetToItem(rs));
			}

			rs.close();
			ps.close();
		} catch( SQLException ex) {
			log.error("Problem iterating over list of items: " + ex.getMessage());
		}

		return list;
	}



	/**
	 * Get first category of an item.
	 * @param itemId
	 * @return category name or empty string
	 */
	public String getItemCategory(int itemId){

		/**
		 * This method is an overkill.
		 * We just want to demonstrate that generally bad decisions in terms of schema are troublesome,
		 * regardless of the underlying database technology.
		 */

		String sqlQuery = "SELECT categories_name as category FROM items_has_categories WHERE items_id = ? LIMIT 1";
		String category = "";

		try{
			PreparedStatement ps = this.connection.prepareStatement(sqlQuery);
			ps.setInt(1, itemId);
			ResultSet rs = ps.executeQuery();

			while(rs.next()){
				category = rs.getString("category");
				break;
			}

			rs.close();
			ps.close();
		} catch( SQLException ex) {
			log.error("Problem iterating over list of items: " + ex.getMessage());
		}

		return category;
	}



	/**
	 * Get items using range based pagination, using the after value
	 *
	 * @param after
	 * @return
	 */
	public List<Item> getItemsRangeBased(String before, String after) {
		List<Item> items = new ArrayList<>();

		// Only one item is passed in, before or after, formulate query based on that item
		int limit = ITEMS_PER_PAGE + 1;

		String sqlQuery = "SELECT * FROM items WHERE id > ? ORDER BY id ASC LIMIT ?";
		// the after or before item id that we need to query for.
		int position = Utils.getIntFromString(after);


		// Use $lte before
		if (before != null && !before.trim().equals("")) {
			position = Utils.getIntFromString(before);
			sqlQuery = "SELECT * FROM items WHERE id < ? ORDER BY id DESC LIMIT ?";

		}

		try{
			PreparedStatement ps = this.connection.prepareStatement(sqlQuery);
			ps.setInt(1, position);
			ps.setInt(2, limit);
			ResultSet rs = ps.executeQuery();

			while(rs.next()){
				items.add(resultSetToItem(rs));
			}

			rs.close();
			ps.close();
		} catch (SQLException ex) {
			log.error("Problem getItemsRangeBased: " + ex.getMessage());
		}

		return items;
	}

	/**
	 * Get number of items, useful for pagination
	 *
	 * @return
	 */
	public long getItemsCount() {
		String sqlQuery = "SELECT COUNT(1) count FROM ITEMS";
		long count = 0;
		try{
			Statement stm = this.connection.createStatement();
			ResultSet rs = stm.executeQuery(sqlQuery);
			while (rs.next()){
				return rs.getLong("count");
			}
		} catch (SQLException ex) {
			log.error("Problem getItemsCount: " + ex.getMessage());
		}

		return count;

	}

	/**
	 * Get items by category, and page (starting at 0)
	 *
	 * @param category
	 * @param page_str
	 * @return
	 */
	public List<Item> getItemsByCategory(String category, String page_str) {
		ArrayList<Item> items = new ArrayList<>();

		String sqlQuery = "SELECT i.* FROM items i, items_has_categories ic WHERE i.id = ic.items_id AND ic.categories_name = ?";

		try {

			PreparedStatement ps = this.connection.prepareStatement(sqlQuery);
			ps.setString(1, category);
			ResultSet rs = ps.executeQuery();

			while(rs.next()){
				items.add( resultSetToItem(rs));
			}

			rs.close();
			ps.close();

		} catch (SQLException ex){
			log.error("Issue return item per category count: " + ex.getMessage());
		}

		return items;
	}

	/**
	 * Get number of items in a category, useful for pagination
	 *
	 * @param category
	 * @return
	 */
	public long getItemsByCategoryCount(String category) {
		String sqlQuery = "SELECT COUNT(*) as count FROM items_has_categories WHERE categories_name = ?";
		long count = 0L;

		try {

			PreparedStatement ps = this.connection.prepareStatement(sqlQuery);
			ps.setString(1, category);
			ResultSet rs = ps.executeQuery();

			while(rs.next()){
				category = rs.getString("count");
				break;
			}

			rs.close();
			ps.close();

		} catch (SQLException ex){
			log.error("Issue return item per category count: " + ex.getMessage());
		}

		return count;
	}

	/**
	 * Text search, requires the index:
	 *      db.item.createIndex( { "title" : "text", "slogan" : "text", "description" : "text" } )
	 *
	 * @param query_str
	 * @param page_str
	 * @return
	 */
	public List<Item> textSearch(String query_str, String page_str) {
		ArrayList<Item> items = new ArrayList<>();
		// TODO missing

		return items;
	}

	/**
	 * Get count for text search results, useful for pagination
	 *
	 * @param query_str
	 * @return
	 */
	public long textSearchCount(String query_str) {
		//TODO missing
		return 0L;
	}

	/**
	 * Use aggregation to get a count of the number of products in each category
	 *
	 * @return
	 */
	public ArrayList<Category> getCategoriesAndNumProducts() {
		ArrayList<Category> categories = new ArrayList<>();

		String sqlQuery = " SELECT categories_name, SUM(1) as sum "
				+ "FROM items_has_categories GROUP BY categories_name "
				+ "ORDER BY categories_name ASC ";
		int total_count = 0;

		try {
			Statement stm = this.connection.createStatement();
			ResultSet rs = stm.executeQuery(sqlQuery);

			while (rs.next()){
				int c = rs.getInt("sum");
				categories.add(new Category( rs.getString("categories_name"), c));
				total_count += c;
			}

			rs.close();
			stm.close();
		} catch (SQLException ex){
			log.error("Issue getting category product count: " + ex.getMessage());
		}


		categories.add(0, new Category("All", total_count));
		return categories;
	}

	/**
	 * Add a review to an item
	 *
	 * @param itemid
	 * @param review
	 */
	public void addReview(Review review, int avg_stars, int itemid) {

		String sqlInsert = "INSERT INTO reviews (name, date, comment, stars, items_id) "
				+ "VALUES (?,?,?,?,?)";

		try{
			PreparedStatement insertItemReview = this.connection.prepareStatement(sqlInsert);
			insertItemReview.setString(1, review.getName());
			insertItemReview.setDate(2, new Date(review.getDate().getTime()));
			insertItemReview.setString(3, review.getComment());
			insertItemReview.setInt(4, review.getStars());
			insertItemReview.setInt(5, itemid);

			insertItemReview.execute();

			insertItemReview.close();

		} catch (SQLException ex){
			log.error("Issue adding a review: " + ex.getMessage());
		}


	}

	/**
	 * Return the constant ITEMS_PER_PAGE
	 *
	 * @return
	 */
	public int getItemsPerPage() {
		return ITEMS_PER_PAGE;
	}

	/**
	 * Returns an Item per ResultSet entry
	 * @param rs
	 * @return
	 * @throws SQLException
	 */
	private Item resultSetToItem(ResultSet rs) throws SQLException{
		Item it = new Item();
		if(rs != null){
			it.setId(rs.getInt("id"));
			it.setTitle(rs.getString("title"));
			it.setDescription(rs.getString("description"));
			it.setPrice(rs.getDouble("price"));
			it.setStars(rs.getInt("stars"));
			it.setSlogan(rs.getString("slogan"));
			it.setQuantity(rs.getInt("quantity"));
			it.setImg_url(rs.getString("img_url"));
			it.setCategory( getItemCategory(rs.getInt("id"))  );
		}
		return it;
	}

}
