package doridlens.neo4j;

import org.neo4j.cypher.CypherException;
import org.neo4j.graphdb.Result;
import org.neo4j.graphdb.Transaction;

import java.io.IOException;

/**
 * Author: MaoMorn
 * Date: 2020/1/2
 * Time: 9:39
 * Description:
 */
public class ARGB8888Query extends Query {

    private ARGB8888Query(QueryEngine queryEngine) {
        super(queryEngine);
    }

    public static ARGB8888Query createARGB8888Query(QueryEngine queryEngine) {
        return new ARGB8888Query(queryEngine);
    }

    @Override
    public void execute(boolean details) throws CypherException, IOException {
        try (Transaction ignored = graphDatabaseService.beginTx()) {
            String query = "MATCH (e: ExternalArgument) WHERE EXISTS(e.is_argb_8888) RETURN e";
            if (details) {
                query += ", count(e) as ARGB8888";
            }
            Result result = graphDatabaseService.execute(query);
            queryEngine.resultToCSV(result, "_ARGB8888.csv");
        }
    }

}
