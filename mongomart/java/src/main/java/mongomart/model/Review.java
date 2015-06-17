package mongomart.model;

import org.bson.*;
import org.bson.codecs.*;
import org.bson.types.ObjectId;

import java.util.Date;

/**
 * Review model object
 */
public class Review implements CollectibleCodec<Review> {
    ObjectId id;
    String name;
    Date date;
    String comment;
    int stars;

    private Codec<Document> reviewCodec;

    public Review() {
        this.reviewCodec = new DocumentCodec();
    }

    public Review(Codec<Document> reviewCodec) {
        this.reviewCodec = reviewCodec;
    }

    @Override
    public void encode(final BsonWriter writer, final Review value, final EncoderContext encoderContext) {
        Document document = new Document();
        document.append("_id", value.id);
        document.append("name", value.name);
        document.append("date", value.date);
        document.append("comment", value.comment);
        document.append("stars", value.stars);
        reviewCodec.encode(writer, document, encoderContext);
    }

    @Override
    public Review decode(final BsonReader reader, final DecoderContext decoderContext) {
        Document document = reviewCodec.decode(reader, decoderContext);
        Review review = new Review();
        review.setId(document.getObjectId("_id"));
        review.setName(document.getString("name"));
        review.setDate(document.getDate("date"));
        review.setComment(document.getString("comment"));
        review.setStars(document.getInteger("stars"));
        return review;
    }

    @Override
    public Class<Review> getEncoderClass() {
        return Review.class;
    }

    @Override
    public Review generateIdIfAbsentFromDocument(Review review)
    {
        if (!documentHasId(review))
        {
            id = new ObjectId();
        }
        return review;
    }

    @Override
    public boolean documentHasId(Review review)
    {
        return review.getId() == null;
    }

    @Override
    public BsonValue getDocumentId(Review review)
    {
        if (review.getId() == null)
        {
            throw new IllegalStateException("The document does not contain an _id");
        }

        return new BsonObjectId(review.getId());
    }

    public ObjectId getId() {
        return id;
    }

    public void setId(ObjectId id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Date getDate() {
        return date;
    }

    public void setDate(Date date) {
        this.date = date;
    }

    public String getComment() {
        return comment;
    }

    public void setComment(String comment) {
        this.comment = comment;
    }

    public int getStars() {
        return stars;
    }

    public void setStars(int stars) {
        this.stars = stars;
    }

    public void populateDummyValues() {
        name = "Jason";
        comment = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.";
        date = new Date();
        stars = 3;
    }
}
