package doridlens.metrics;

import doridlens.entity.DoridlensExternalArgument;

/**
 * Author: MaoMorn
 * Date: 2020/1/2
 * Time: 13:55
 * Description:
 */
public class ArgumentMetrics {
    public static void createIsARGB8888(DoridlensExternalArgument argument, boolean value) {
        argument.addMetric("is_argb_8888", value);
    }
}
