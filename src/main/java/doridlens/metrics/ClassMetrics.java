package doridlens.metrics;

import doridlens.entity.DoridlensClass;

/**
 * Author: MaoMorn
 * Date: 2020/1/2
 * Time: 10:45
 * Description:
 */
public class ClassMetrics {
    public static void createIsApplication(DoridlensClass entity, boolean value) {
        entity.addMetric("is_application", value);
    }

    public static void createIsActivity(DoridlensClass entity, boolean value) {
        entity.addMetric("is_activity", value);
    }

    public static void createIsService(DoridlensClass entity, boolean value) {
        entity.addMetric("is_service", value);
    }

    public static void createIsInterface(DoridlensClass entity, boolean value) {
        entity.addMetric("is_interface", value);
    }

    public static void createIsInnerClass(DoridlensClass entity, boolean value) {
        entity.addMetric("is_inner_class", value);
    }

    public static void createIsContentProvider(DoridlensClass entity, boolean value) {
        entity.addMetric("is_content_provider", value);
    }

    public static void createIsBroadcastReceiver(DoridlensClass entity, boolean value) {
        entity.addMetric("is_broadcast_receiver", value);
    }

    public static void createIsBitmap(DoridlensClass entity, boolean value) {
        entity.addMetric("is_bitmap", value);
    }

    public static void createIsView(DoridlensClass entity, boolean value) {
        entity.addMetric("is_view", value);
    }

    public static void createIsAsyncTask(DoridlensClass entity, boolean value) {
        entity.addMetric("is_async_task", value);
    }

    public static void createCouplingBetweenObjects(DoridlensClass entity) {
        entity.addMetric("coupling_between_object_classes", entity.getCouplingValue());
    }

    public static void createLackofCohesionInMethods(DoridlensClass entity) {
        entity.addMetric("lack_of_cohesion_in_methods", entity.computeLCOM());
    }

    public static void createNPathComplexity(DoridlensClass entity) {
        entity.addMetric("npath_complexity", entity.computeNPathComplexity());
    }

    public static void createClassComplexity(DoridlensClass entity) {
        entity.addMetric("class_complexity", entity.getComplexity());
    }

    public static void createDepthOfInheritance(DoridlensClass entity, int value) {
        entity.addMetric("depth_of_inheritance", value);
    }

    public static void createNumberOfImplementedInterfaces(DoridlensClass entity, int value) {
        entity.addMetric("number_of_implemented_interfaces", value);
    }

    public static void createNumberOfAttributes(DoridlensClass entity, int value) {
        entity.addMetric("number_of_attributes", value);
    }

    public static void createNumberOfChildren(DoridlensClass entity) {
        entity.addMetric("number_of_children", entity.getChildren());
    }
}
