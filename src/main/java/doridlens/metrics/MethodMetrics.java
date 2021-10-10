package doridlens.metrics;

import doridlens.entity.Entity;
import doridlens.entity.DoridlensMethod;

/**
 * Author: MaoMorn
 * Date: 2020/1/2
 * Time: 10:51
 * Description:
 */
public class MethodMetrics {
    public static void createIsOverride(DoridlensMethod method, boolean value) {
        method.addMetric("is_override", value);
    }

    public static void createIsSynchronized(DoridlensMethod method, boolean value) {
        method.addMetric("is_synchronized", value);
    }

    public static void createIsInit(DoridlensMethod method, boolean value) {
        method.addMetric( "is_init", value);
    }

    public static void createIsGetter(DoridlensMethod method, boolean value) {
        method.addMetric( "is_getter", value);
    }

    public static void createIsSetter(DoridlensMethod method, boolean value) {
        method.addMetric( "is_setter", value);
    }

    public static void createCyclomaticComplexity(DoridlensMethod method, int value) {
        method.addMetric("cyclomatic_complexity", value);
    }

    public static void createNumberOfParameters(DoridlensMethod method, int value) {
        method.addMetric( "number_of_parameters", value);
    }

    public static void createNumberOfInstructions(DoridlensMethod method, int value) {
        method.addMetric( "number_of_instructions", value);
    }

    public static void createNumberOfDirectCalls(DoridlensMethod method, int value) {
        method.addMetric( "number_of_direct_calls", value);
    }

    public static void createNumberOfCallers(DoridlensMethod method, int value) {
        method.addMetric( "number_of_callers", value);
    }

    public static void createNumberOfDeclaredLocals(DoridlensMethod method, int value) {
        method.addMetric( "number_of_declared_locals", value);
    }
}
