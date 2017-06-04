package mongomart.model;

import java.util.Date;

import org.bson.types.ObjectId;

/**
 * Review model object
 */
public class Review {
    int id = -1;
    String name;
    Date date;
    String comment;
    int stars;
    int itemid;
    ObjectId _id;

    public Review() {

    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
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

    public int getItemid() {
        return itemid;
    }

    public void setItemid(int itemid) {
        this.itemid = itemid;
    }

    public void populateDummyValues() {
        name = "Jason";
        comment = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.";
        date = new Date();
        stars = 3;
    }

    public void set_Id(ObjectId _id){
    	this._id = _id;
    }
    
    public ObjectId get_Id(){
    	return this._id;
    }
    
    
	@Override
	public boolean equals(Object obj) {
		
		if (this == obj){
			return true;
		}
		
		if ((obj == null) || (obj.getClass() != this.getClass())){
			return false;
		}
		
		Review review = (Review)obj;
		
		if (this.id > 0 ){
			return review.id == this.id;
		}
		
		if ( (review._id != null)){
			return review._id.equals(this._id);
		}
		
		return this.name == review.name && this.itemid == review.itemid 
				&& this.stars == review.stars && this.comment == review.comment;
		
	}
    
	
	public int hashCode(){
		int hash = 27017;
		return ( hash * stars * name.hashCode() * comment.hashCode() ) + (id * itemid) ;
	}
    
    
}
