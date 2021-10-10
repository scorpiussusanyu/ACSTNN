package doridlens.entity;

import java.util.HashMap;

/**
 * Author: MaoMorn
 * Date: 2020/1/2
 * Time: 9:17
 * Description:
 */
public class Entity {
    protected String name;
    //    protected List<Metric> metrics = new ArrayList<>();
    protected HashMap<String, Object> metrics = new HashMap<>();

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public HashMap<String, Object> getMetrics() {
        return metrics;
    }

    public void addMetric(String name, Object value) {
        this.metrics.put(name, value);
    }

    @Override
    public String toString() {
        return name;
    }
}
