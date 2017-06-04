package mongomart;

import static spark.SparkBase.port;
import static spark.SparkBase.staticFileLocation;

import java.io.IOException;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

import mongomart.controller.CartController;
import mongomart.controller.LocationsController;
import mongomart.controller.StoreController;

import com.mongodb.MongoClient;

import freemarker.template.Configuration;

/**
 * Main MongoMart class
 *
 * To run:
 *      Ensure the dataset from data/ has been imported to your Database (instructions located in README.md)
 *      Run the main method below
 *      Open http://localhost:8080
 */
public class MongoMart {
    public static final int HTTP_PORT = 8080;  // HTTP port to listen for requests on
    
    private MongoClient mongoClient;
    /**
     * Main method for MongoMart application
     *
     * @param args
     * @throws IOException
     */

    public static void main(String[] args) throws IOException {

        try {
            // The newInstance() call is a work around for some
            // broken Java implementations
            Class.forName("com.mysql.jdbc.Driver").newInstance();

            String connectionString = "jdbc:mysql://localhost/mongomart?user=root";
            if (args.length != 0) {
                connectionString = args[0];
            }

            new MongoMart(connectionString);

        } catch (Exception ex) {
            System.out.println("Bad things happen: " + ex.getMessage());
        }

    }


    /**
     * Create an instance of MongoMart
     *
     * @param connectionString
     * @throws IOException
     */
    public MongoMart(String connectionString) throws IOException {

        // Create a Database connection
        try{
            Connection connection = DriverManager.getConnection(connectionString);
            // Freemarker configuration
            final Configuration cfg = createFreemarkerConfiguration();

            // MongoClient connection
            mongoClient = new MongoClient();

            port(HTTP_PORT);
            staticFileLocation("/assets");

            // Start controllers
            //AdminController adminController = new AdminController(cfg, itemDatabase);
            StoreController storeController = new StoreController(cfg, connection, mongoClient.getDatabase("mongomart"));
            CartController cartController = new CartController(cfg, connection);
            LocationsController locationsController = new LocationsController(cfg, connection);

        }catch(SQLException ex){
            System.out.println("Bad things happen: " + ex.getMessage());
        }
    }

    /**
     *
     * @return
     */
    private Configuration createFreemarkerConfiguration() {
        Configuration retVal = new Configuration();
        retVal.setClassForTemplateLoading(MongoMart.class, "/freemarker");
        return retVal;
    }
}
