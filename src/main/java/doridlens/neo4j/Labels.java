package doridlens.neo4j;

import org.neo4j.graphdb.Label;

/**
 * Author: MaoMorn
 * Date: 2020/1/2
 * Time: 9:43
 * Description:
 */
public enum Labels implements Label {
    App,
    Class,
    Variable,
    Method,
    Argument,
    ExternalClass,
    ExternalMethod,
    ExternalArgument
}
