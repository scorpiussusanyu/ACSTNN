package doridlens.metrics;

import doridlens.entity.Entity;

/**
 * Author: MaoMorn
 * Date: 2020/1/2
 * Time: 11:08
 * Description:
 */
public class CommonMetrics {
    public static void createIsAbstract(Entity entity, boolean value) {
        entity.addMetric("is_abstract", value);
    }

    public static void createIsFinal(Entity entity, boolean value) {
        entity.addMetric("is_final", value);
    }

    public static void createIsStatic(Entity entity, boolean value) {
        entity.addMetric("is_static", value);
    }

    public static void createNumberOfMethods(Entity entity, int value) {
        entity.addMetric("number_of_methods", value);
    }
}
