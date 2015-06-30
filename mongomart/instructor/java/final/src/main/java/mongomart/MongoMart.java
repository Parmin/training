package mongomart;

import com.mongodb.MongoClient;
import com.mongodb.MongoClientURI;
import com.mongodb.client.MongoDatabase;
import freemarker.template.Configuration;
import mongomart.controller.AdminController;
import mongomart.controller.CartController;
import mongomart.controller.StoreController;

import java.io.IOException;

import static spark.SparkBase.port;
import static spark.SparkBase.staticFileLocation;

/**
 * Main MongoMart class
 *
 * To run:
 *      Ensure the dataset from data/ has been imported to your MongoDB instance (instructions located in README.md)
 *      Run the main method below
 *      Open http://localhost:8080
 */
public class MongoMart {
    public static final int HTTP_PORT = 8080;  // HTTP port to listen for requests on

    /**
     * Main method for MongoMart application
     *
     * @param args
     * @throws IOException
     */

    public static void main(String[] args) throws IOException {
        if (args.length == 0) {
            new MongoMart("mongodb://localhost:27017,localhost:27018,localhost:27019");
        }
        else {
            new MongoMart(args[0]);
        }
    }

    /**
     * Create an instance of MongoMart
     *
     * @param mongoURIString
     * @throws IOException
     */

    public MongoMart(String mongoURIString) throws IOException {
        // Create MongoDB connection
        final MongoClient mongoClient = new MongoClient(new MongoClientURI(mongoURIString));
        final MongoDatabase itemDatabase = mongoClient.getDatabase("mongomart");

        // Freemarker configuration
        final Configuration cfg = createFreemarkerConfiguration();

        port(HTTP_PORT);
        staticFileLocation("/assets");

        // Start controllers
        AdminController adminController = new AdminController(cfg, itemDatabase);
        StoreController storeController = new StoreController(cfg, itemDatabase);
        CartController cartController = new CartController(cfg, itemDatabase);

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
