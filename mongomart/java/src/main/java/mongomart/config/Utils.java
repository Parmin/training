package mongomart.config;

/**
 * Created by jason on 6/15/15.
 */
public class Utils {
    public static int getIntFromString(String src) {
        int returnValue = 0;

        try {  returnValue = (new Integer(src)); }
        catch (Exception e) {  }

        return returnValue;
    }
}
