package mongomart.model;

import org.bson.*;
import org.bson.codecs.*;
import org.bson.types.ObjectId;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

/**
 * Created by jason on 6/16/15.
 */
public class Cart  implements CollectibleCodec<Cart> {
    ObjectId id;
    String status;
    Date last_modified;
    String userid;
    List<Item> items;

    private Codec<Document> cartCodec;

    public Cart() {
        this.cartCodec = new DocumentCodec();
    }

    public Cart(Codec<Document> cartCodec) {
        this.cartCodec = cartCodec;
    }

    @Override
    public void encode(final BsonWriter writer, final Cart value, final EncoderContext encoderContext) {
        Document document = new Document();
        document.append("_id", value.id);
        document.append("status", value.status);
        document.append("last_modified", value.last_modified);
        document.append("userid", value.userid);
        document.append("items", value.items);
        cartCodec.encode(writer, document, encoderContext);
    }

    @Override
    public Cart decode(final BsonReader reader, final DecoderContext decoderContext) {
        Document document = cartCodec.decode(reader, decoderContext);

        Cart cart = new Cart();
        cart.setId(document.getObjectId("_id"));
        cart.setStatus(document.getString("status"));
        cart.setLast_modified(document.getDate("last_modified"));
        cart.setUserid(document.getString("userid"));
        if (document.containsKey("items") && document.get("items") instanceof List) {
            List<Item> items = new ArrayList<>();
            List<Document> itemsList = (List<Document>)document.get("items");

            for (Document itemDoc : itemsList) {
                Item item = new Item();

                if (itemDoc.containsKey("_id")) {
                    item.setId(itemDoc.getInteger("_id"));
                }

                if (itemDoc.containsKey("quantity")) {
                    item.setQuantity(itemDoc.getInteger("quantity"));
                }

                if (itemDoc.containsKey("title")) {
                    item.setTitle(itemDoc.getString("title"));
                }

                if (itemDoc.containsKey("img_url")) {
                    item.setImg_url(itemDoc.getString("img_url"));
                }

                if (itemDoc.containsKey("price")) {
                    item.setPrice(itemDoc.getDouble("price"));
                }

                items.add(item);
            }

            cart.setItems(items);
        }
        else {
            cart.setItems(new ArrayList<Item>());
        }

        return cart;
    }

    @Override
    public Class<Cart> getEncoderClass() {
        return Cart.class;
    }

    @Override
    public Cart generateIdIfAbsentFromDocument(Cart cart)
    {
        if (!documentHasId(cart))
        {
            cart.setId(new ObjectId());
        }
        return cart;
    }

    @Override
    public boolean documentHasId(Cart cart)
    {
        return cart == null;
    }

    @Override
    public BsonObjectId getDocumentId(Cart cart)
    {
        if (id == null)
        {
            throw new IllegalStateException("The document does not contain an _id");
        }

        return new BsonObjectId(cart.getId());
    }

    public ObjectId getId() {
        return id;
    }

    public void setId(ObjectId id) {
        this.id = id;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public Date getLast_modified() {
        return last_modified;
    }

    public void setLast_modified(Date last_modified) {
        this.last_modified = last_modified;
    }

    public String getUserid() {
        return userid;
    }

    public void setUserid(String userid) {
        this.userid = userid;
    }

    public List<Item> getItems() {
        return items;
    }

    public void setItems(List<Item> items) {
        this.items = items;
    }
}
