package mongomart.dao.rdbms;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

import mongomart.model.Cart;
import mongomart.model.Item;

/**
 * All database access to the "cart" collection
 */
public class CartDao {
    private Log log = LogFactory.getLog(CartDao.class);
    private final Connection connection;

    /**
     *
     * @param connection
     */
    public CartDao(final Connection connection) {
        this.connection = connection;
    }

    /**
     * Get a cart by userid
     *
     * @param userid
     * @return
     */
    public Cart getCart(String userId) {
        Cart cart = getCartDetails(userId);

        if(cart.getId() < 0) {
            createCart(userId);
            cart = getCartDetails(userId);
        }

        return cart;
    }


    private Cart getCartDetails(String userId) {
        String sqlQuery = "SELECT * FROM carts WHERE user_id = ? LIMIT 1";
        Cart cart = new Cart();
        boolean cartFound = false;
        try {

            PreparedStatement ps = this.connection.prepareStatement(sqlQuery);
            ps.setString(1, userId);
            ResultSet rs = ps.executeQuery();

            while(rs.next()) {
                cart = this.resultSetToCart(rs);
                cartFound = true;
                break;
            }

            rs.close();
            ps.close();
        } catch(SQLException ex) {
            log.error("Problem wiht getCart: " + ex.getMessage());
        }

        if (cartFound) {
            populateCartItems(cart);
        } else {
            log.info("NO CART FOUND ... creating one");
        }

        return cart;
    }


    private void populateCartItems(Cart cart) {

        String sqlQuery = "SELECT i.*, ci.quantity as QTY FROM carts_has_items ci, items i " +
            "WHERE i.id = ci.items_id AND ci.carts_id = ?";

        try {

            PreparedStatement ps = this.connection.prepareStatement(sqlQuery);
            ps.setInt(1, cart.getId());
            ResultSet rs = ps.executeQuery();

            cart.setItems(this.resultSetToItems(rs));

            rs.close();
            ps.close();

        } catch (SQLException ex) {
            log.error("Problem wiht populating cart items: " + ex.getMessage());
        }

    }

    /**
     * Add an item to a cart
     *
     * @param item
     * @param userid
     */

    public void addToCart(Item item, String userid) {
        Cart cart = getCart(userid);

        if (existsInCart(item.getId(), userid)) {
            for (Item it : cart.getItems()) {
              if (it == item) {
                this.updateQuantity(it.getQuantity()+1, item.getId(), cart.getId() );
                break;
              }
            }

        } else {

            String sqlInsert = "INSERT INTO carts_has_items (items_id, carts_id, quantity) VALUES(?, ?, ?)";

            try {
                PreparedStatement ps = this.connection.prepareStatement(sqlInsert);
                ps.setInt(1, item.getId());
                ps.setInt(2, cart.getId());
                ps.setInt(3, item.getQuantity());
                ps.execute();
                ps.close();
            } catch (SQLException ex) {
                log.error("Problem adding to cart: " + ex.getMessage());
            }
        }
    }


    private void dropItem(int itemId, int cartId) {
        String sqlDelete = "DELETE FROM carts_has_items WHERE items_id = ? AND carts_id = ?";

        try {
            PreparedStatement ps  = this.connection.prepareStatement(sqlDelete);
            ps.setInt(1, itemId);
            ps.setInt(2, cartId);
            ps.execute();
            ps.close();
        } catch(SQLException ex) {
            log.error("Problem dropping item: " + ex.getMessage());
        }
    }


    private void updateQuantity(int quantity, int itemId, int cartId) {
        String sqlUpdate = "UPDATE carts_has_items SET quantity = ? WHERE items_id = ? AND carts_id = ?";

        try {
            PreparedStatement ps  = this.connection.prepareStatement(sqlUpdate);
            ps.setInt(1, quantity);
            ps.setInt(2, itemId);
            ps.setInt(3, cartId);
            ps.execute();
            ps.close();
        } catch(SQLException ex) {
            log.error("Problem updating quantity in cart: " + ex.getMessage());
        }
    }

    private void addToCart(int quantity, int itemId, int cartId) {

        String sqlInsert = "INSERT INTO carts_has_items (quantity, items_id, carts_id) VALUES (?, ?, ?)";

        try {
            PreparedStatement ps  = this.connection.prepareStatement(sqlInsert);
            ps.setInt(1, quantity);
            ps.setInt(2, itemId);
            ps.setInt(3, cartId);
            ps.execute();
            ps.close();
        } catch(SQLException ex) {
            log.error("Problem updating quantity in cart: " + ex.getMessage());
        }
    }


    public void createCart(String userId) {
        String sqlInsert = "INSERT INTO carts (user_id, status, last_modified) VALUES (?,?,?)";

        try {
            Date now = new Date();
            PreparedStatement ps = this.connection.prepareStatement(sqlInsert);
            ps.setString(1, userId);
            ps.setString(2, "open");
            ps.setDate(3,  new java.sql.Date(now.getTime()));
            ps.execute();
            ps.close();
        } catch (SQLException ex) {
            log.error("Issue creating cart: "+ ex.getMessage());
        }

    }

    /**
     * Update the quantity of an item in a cart.  If quantity is 0, remove item from cart
     *
     * @param itemId
     * @param quantity
     * @param userId
     */
    public void updateQuantity(int itemId, int quantity, String userId) {

        Cart cart = getCart(userId);

        if (cart.getId() < 1) {
            createCart(userId);
            cart = getCart(userId);
        }

        if(quantity < 1) {
            dropItem(itemId, cart.getId());
            return;
        }

        if (existsInCart(itemId, userId)) {
            updateQuantity(quantity, itemId, cart.getId());
            return;
        }
        addToCart(quantity, itemId, cart.getId());
    }

    /**
     * Determine if an item is already in a cart, useful for when "Add to cart" has been clicked for an existing item
     * in the user's cart, then the quantity just be incremented by 1
     *
     * @param itemid
     * @param userid
     * @return
     */
    public boolean existsInCart(int itemid, String userid) {
        boolean exists = false;
        String sqlQuery = "SELECT SUM(1) as sum FROM carts_has_items ci, carts c "+
            "WHERE ci.carts_id = c.id AND c.user_id = ? AND ci.items_id = ?";

        try {
            PreparedStatement ps = this.connection.prepareStatement(sqlQuery);
            ps.setString(1, userid);
            ps.setInt(2, itemid);
            ResultSet rs = ps.executeQuery();

            while(rs.next()) {
                exists = rs.getInt("sum") >= 1;
                break;
            }
            rs.close();
            ps.close();
        } catch(SQLException ex) {
            log.error("Issue on exists in cart: "+ ex.getMessage());
        }

        return exists;
    }


    private List<Item> resultSetToItems(ResultSet rs) throws SQLException {
        List<Item> items = new ArrayList<Item>();

        while(rs.next()) {
            Item it = new Item();
            it.setId(rs.getInt("id"));
            it.setTitle(rs.getString("title"));
            it.setDescription(rs.getString("description"));
            it.setPrice(rs.getDouble("price"));
            it.setStars(rs.getInt("stars"));
            it.setSlogan(rs.getString("slogan"));
            it.setQuantity(rs.getInt("QTY"));
            it.setImg_url(rs.getString("img_url"));
            items.add(it);
        }

        return items;
    }


    private Cart resultSetToCart(ResultSet rs) throws SQLException {
        Cart cart = new Cart();

        if (rs != null) {
            cart.setId(rs.getInt("id"));
            cart.setLast_modified(new Date(rs.getDate("last_modified").getTime()));
            cart.setStatus(rs.getString("status"));
            cart.setUserid(rs.getString("user_id"));
        }

        return cart;

    }
}
