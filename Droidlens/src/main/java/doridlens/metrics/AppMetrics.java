package doridlens.metrics;

import doridlens.entity.DoridlensApp;

/**
 * Author: MaoMorn
 * Date: 2020/1/2
 * Time: 10:44
 * Description:
 */
public class AppMetrics {
    public static void createNumberOfViews(DoridlensApp entity, int value) {
        entity.addMetric("number_of_views", value);
    }

    public static void createNumberOfVariables(DoridlensApp entity, int value) {
        entity.addMetric("number_of_variables", value);
    }

    public static void createNumberOfServices(DoridlensApp entity, int value) {
        entity.addMetric("number_of_services", value);
    }

    public static void createNumberOfInterfaces(DoridlensApp entity, int value) {
        entity.addMetric("number_of_interfaces", value);
    }

    public static void createNumberOfInnerClasses(DoridlensApp entity, int value) {
        entity.addMetric("number_of_inner_classes", value);
    }

    public static void createNumberOfAbstractClasses(DoridlensApp entity, int value) {
        entity.addMetric("number_of_abstract_classes", value);
    }

    public static void createNumberOfBroadcastReceivers(DoridlensApp entity, int value) {
        entity.addMetric("number_of_broadcast_receivers", value);
    }

    public static void createNumberOfAsyncTasks(DoridlensApp entity, int value) {
        entity.addMetric("number_of_async_tasks", value);
    }

    public static void createNumberOfArgb8888(DoridlensApp entity, int value) {
        entity.addMetric("number_of_argb_8888", value);
    }

    public static void createNumberOfActivities(DoridlensApp entity, int value) {
        entity.addMetric("number_of_activities", value);
    }

    public static void createNumberOfClasses(DoridlensApp entity, int value) {
        entity.addMetric("number_of_classes", value);
    }

    public static void createNumberOfContentProviders(DoridlensApp entity, int value) {
        entity.addMetric("number_of_content_providers", value);
    }
}
