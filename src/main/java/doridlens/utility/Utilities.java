package doridlens.utility;

import java.io.FileInputStream;
import java.io.InputStream;
import java.io.InputStreamReader;

/**
 * Author: MaoMorn
 * Date: 2020/1/2
 * Time: 19:46
 * Description:
 */
public class Utilities {
    public static String readFile(String fileName) {
        InputStreamReader isr = null;
        StringBuilder sb = new StringBuilder();
        char[] buf = new char[1024];
        try {
            InputStream is = new FileInputStream(fileName);
            isr = new InputStreamReader(is);
            int len;
            while ((len = isr.read(buf)) > 0) {
                sb.append(buf, 0, len);
            }
            isr.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
        return sb.toString();
    }
}
