package doridlens.neo4j;

import org.neo4j.cypher.CypherException;
import org.neo4j.graphdb.GraphDatabaseService;

import java.io.IOException;

/**
 * Author: MaoMorn
 * Date: 2020/1/2
 * Time: 9:39
 * Description:
 */
public abstract class Query {
    protected QueryEngine queryEngine;
    protected GraphDatabaseService graphDatabaseService;

    public Query(QueryEngine queryEngine) {
        this.queryEngine = queryEngine;
        graphDatabaseService = queryEngine.getGraphDatabaseService();
    }

    public abstract void execute(boolean details) throws CypherException, IOException;
}
