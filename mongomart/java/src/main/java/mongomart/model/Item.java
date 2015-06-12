package mongomart.model;

import org.bson.*;
import org.bson.codecs.*;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by jason on 6/9/15.
 */
public class Item implements CollectibleCodec<Item> {
    int id = 0;
    String title;
    String description;
    String category;
    double price;
    int stars;
    String img_url;
    String slogan;
    List<Review> reviews;

    private Codec<Document> itemCodec;

    public Item() {
        this.itemCodec = new DocumentCodec();
    }

    public Item(Codec<Document> itemCodec) {
        this.itemCodec = itemCodec;
    }

    @Override
    public void encode(final BsonWriter writer, final Item value, final EncoderContext encoderContext) {
        Document document = new Document();
        document.append("_id", value.id);
        document.append("title", value.title);
        document.append("description", value.description);
        document.append("cateogry", value.category);
        document.append("price", value.price);
        document.append("stars", value.stars);
        document.append("img_url", value.img_url);
        document.append("slogan", value.slogan);
        itemCodec.encode(writer, document, encoderContext);
    }

    @Override
    public Item decode(final BsonReader reader, final DecoderContext decoderContext) {
        Document document = itemCodec.decode(reader, decoderContext);

        Item item = new Item();
        item.setId(document.getInteger("_id"));
        item.setTitle(document.getString("title"));
        item.setDescription(document.getString("description"));
        item.setCategory(document.getString("category"));
        item.setPrice(document.getDouble("price"));
        item.setStars(document.getInteger("stars"));
        item.setImg_url(document.getString("img_url"));
        item.setSlogan(document.getString("slogan"));
        if (document.containsKey("reviews") && document.get("reviews") instanceof List) {
            List<Review> reviews = new ArrayList<>();
            List<Document> reviewsList = (List<Document>)document.get("reviews");

            for (Document reviewDoc : reviewsList) {
                Review review = new Review();
                review.setComment(reviewDoc.getString("comment"));
                review.setName(reviewDoc.getString("name"));
                review.setStars(reviewDoc.getInteger("stars"));
                review.setDate(reviewDoc.getDate("date"));
                reviews.add(review);
            }

            item.setReviews(reviews);
        }
        else {
            item.setReviews(new ArrayList<Review>());
        }

        return item;
    }

    @Override
    public Class<Item> getEncoderClass() {
        return Item.class;
    }

    @Override
    public Item generateIdIfAbsentFromDocument(Item item)
    {
        if (!documentHasId(item))
        {
            item.setId(1);
        }
        return item;
    }

    @Override
    public boolean documentHasId(Item item)
    {
        return item.getId() != 0;
    }

    @Override
    public BsonValue getDocumentId(Item item)
    {
        if (id == 0)
        {
            throw new IllegalStateException("The document does not contain an _id");
        }

        return new BsonInt32(item.getId());
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getCategory() {
        return category;
    }

    public void setCategory(String category) {
        this.category = category;
    }

    public double getPrice() {
        return price;
    }

    public void setPrice(double price) {
        this.price = price;
    }

    public List<Review> getReviews() {
        return reviews;
    }

    public void setReviews(List<Review> reviews) {
        this.reviews = reviews;
    }

    public int getStars() {
        return stars;
    }

    public void setStars(int stars) {
        this.stars = stars;
    }

    public String getImg_url() {
        return img_url;
    }

    public void setImg_url(String img_url) {
        this.img_url = img_url;
    }

    public String getSlogan() {
        return slogan;
    }

    public void setSlogan(String slogan) {
        this.slogan = slogan;
    }

    public void populateDummyValues() {
        title = "Lorem ipsum dolor sit amet";
        description = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.";
        category = "Apparel";
        price = 9.99;
        img_url = "/img/products/hoodie.jpg";
        slogan = "Lorem ipsum";
        stars = 4;
        reviews = new ArrayList<Review>();

        Review review = new Review();
        review.populateDummyValues();
        reviews.add(review);
    }
}
