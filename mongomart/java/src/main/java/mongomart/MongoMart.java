package mongomart;

import com.mongodb.MongoClient;
import com.mongodb.MongoClientURI;
import com.mongodb.client.MongoDatabase;
import freemarker.template.Configuration;
import mongomart.controller.AdminController;
import mongomart.controller.StoreController;
import mongomart.model.Item;
import mongomart.model.Review;
import org.bson.Document;
import org.bson.codecs.Codec;
import org.bson.codecs.configuration.CodecRegistries;
import org.bson.codecs.configuration.CodecRegistry;

import java.io.IOException;

import static spark.SparkBase.port;
import static spark.SparkBase.staticFileLocation;

/**
 * Created by jason on 6/9/15.
 */
public class MongoMart {
    public static final int HTTP_PORT = 8080;  // HTTP port to listen for requests on

    public static void main(String[] args) throws IOException {
        if (args.length == 0) {
            new MongoMart("mongodb://localhost");
        }
        else {
            new MongoMart(args[0]);
        }
    }

    public MongoMart(String mongoURIString) throws IOException {
        Codec<Document> defaultDocumentCodec = MongoClient.getDefaultCodecRegistry().get(Document.class);
        Item item = new Item(defaultDocumentCodec);
        Review review = new Review(defaultDocumentCodec);

        CodecRegistry codecRegistry = CodecRegistries.fromRegistries(
                MongoClient.getDefaultCodecRegistry(),
                CodecRegistries.fromCodecs(item),
                CodecRegistries.fromCodecs(review)
        );

        final MongoClient mongoClient = new MongoClient(new MongoClientURI(mongoURIString));
        final MongoDatabase itemDatabase = mongoClient.getDatabase("mongomart").withCodecRegistry(codecRegistry);

        final Configuration cfg = createFreemarkerConfiguration();

        port(HTTP_PORT);
        staticFileLocation("/assets");
        AdminController adminController = new AdminController(cfg, itemDatabase);
        StoreController storeController = new StoreController(cfg, itemDatabase);

    }

    private Configuration createFreemarkerConfiguration() {
        Configuration retVal = new Configuration();
        retVal.setClassForTemplateLoading(MongoMart.class, "/freemarker");
        return retVal;
    }
}
