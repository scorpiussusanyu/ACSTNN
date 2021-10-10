package doridlens.neo4j;

import org.neo4j.graphdb.RelationshipType;

/**
 * Author: MaoMorn
 * Date: 2020/1/2
 * Time: 9:46
 * Description:
 */
public enum RelationTypes implements RelationshipType {
    APP_OWNS_CLASS,
    CLASS_OWNS_METHOD,
    CLASS_OWNS_VARIABLE,
    METHOD_OWNS_ARGUMENT,
    IMPLEMENTS,
    EXTENDS,
    CALLS,
    USES
}
