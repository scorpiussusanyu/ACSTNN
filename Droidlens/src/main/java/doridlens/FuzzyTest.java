package doridlens;

import net.sourceforge.jFuzzyLogic.FIS;
import net.sourceforge.jFuzzyLogic.FunctionBlock;
import net.sourceforge.jFuzzyLogic.plot.JFuzzyChart;

/**
 * Author: MaoMorn
 * Date: 2020/1/2
 * Time: 9:48
 * Description:
 */
public class FuzzyTest {
    public static void main(String[] args) {
        // Load from 'FCL' file
        String fileName = FuzzyTest.class.getResource("/fcl/Blob.fcl").getPath();
        FIS fis = FIS.load(fileName, true);

        if (fis == null) {
            System.err.println("Can't load file: '" + fileName + "'");
            System.exit(1);
        }

        // Get default function block
        FunctionBlock fb = fis.getFunctionBlock(null);
        JFuzzyChart.get().chart(fb);
        int[] lcom = {26, 27, 27, 28, 60, 320, 26, 39}; // 25,40
        int[] nom = {17, 17, 18, 19, 17, 21, 27, 22}; // 14.5,22
        int[] noa = {9, 9, 10, 10, 17, 10, 13, 13}; // 8.5,13
        JFuzzyChart.get().chart(fb);
        for (int i = 0; i < lcom.length; i++) {
            fb.setVariable("lack_of_cohesion_in_methods", lcom[i]);
            fb.setVariable("number_of_methods", nom[i]);
            fb.setVariable("number_of_attributes", noa[i]);
            fb.evaluate();
            JFuzzyChart.get().chart(fb.getVariable("res"), fb.getVariable("res").getDefuzzifier(), true);
            System.out.println("Res (" + lcom[i] + "," + nom[i] + "," + noa[i] + "): " + fb.getVariable("res").getValue());
        }
    }
}
