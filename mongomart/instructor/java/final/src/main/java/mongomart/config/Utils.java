package mongomart.config;

/**
 * Simple utility functions to be used through MongoMart application
 */
public class Utils {
    public static int getIntFromString(String src) {
        int returnValue = 0;

        try {  returnValue = (new Integer(src)); }
        catch (Exception e) {  }

        return returnValue;
    }
}
