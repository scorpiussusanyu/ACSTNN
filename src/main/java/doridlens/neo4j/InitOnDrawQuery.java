package doridlens.neo4j;

import org.neo4j.cypher.CypherException;
import org.neo4j.graphdb.Result;
import org.neo4j.graphdb.Transaction;

import java.io.IOException;

/**
 * Author: MaoMorn
 * Date: 2020/1/2
 * Time: 9:44
 * Description:
 */
public class InitOnDrawQuery extends Query {

    private InitOnDrawQuery(QueryEngine queryEngine) {
        super(queryEngine);
    }

    public static InitOnDrawQuery createInitOnDrawQuery(QueryEngine queryEngine) {
        return new InitOnDrawQuery(queryEngine);
    }

    @Override
    public void execute(boolean details) throws CypherException, IOException {
        try (Transaction ignored = graphDatabaseService.beginTx()) {
            String query = "MATCH (:Class{parent_name:'android.view.View'})-[:CLASS_OWNS_METHOD]->(n:Method{name:'onDraw'})-[:CALLS]->({name:'<init>'}) return n.app_key as app_key";
            if (details) {
                query += ",n.full_name as full_name";
            } else {
                query += ",count(n) as IOD";
            }
            Result result = graphDatabaseService.execute(query);
            queryEngine.resultToCSV(result, "_IOD.csv");
        }
    }
}
