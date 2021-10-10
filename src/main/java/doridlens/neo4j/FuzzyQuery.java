package doridlens.neo4j;

import org.neo4j.cypher.CypherException;

import java.io.IOException;

/**
 * Author: MaoMorn
 * Date: 2020/1/2
 * Time: 9:41
 * Description:
 */
public abstract class FuzzyQuery extends Query {
    protected String fclFile;

    public FuzzyQuery(QueryEngine queryEngine) {
        super(queryEngine);
    }

    public abstract void executeFuzzy(boolean details) throws CypherException, IOException;
}
