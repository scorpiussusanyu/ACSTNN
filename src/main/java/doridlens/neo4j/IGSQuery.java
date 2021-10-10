package doridlens.neo4j;

import org.neo4j.cypher.CypherException;
import org.neo4j.graphdb.Result;
import org.neo4j.graphdb.Transaction;

import java.io.IOException;

/**
 * Author: MaoMorn
 * Date: 2020/1/2
 * Time: 9:42
 * Description:
 */
public class IGSQuery extends Query {

    private IGSQuery(QueryEngine queryEngine) {
        super(queryEngine);
    }

    public static IGSQuery createIGSQuery(QueryEngine queryEngine) {
        return new IGSQuery(queryEngine);
    }

    @Override
    public void execute(boolean details) throws CypherException, IOException {
        try (Transaction ignored = graphDatabaseService.beginTx()) {
            String query = "MATCH (a:App) WITH a.app_key as key MATCH (cl:Class {app_key: key})-[:CLASS_OWNS_METHOD]->(m1:Method {app_key: key})-[:CALLS]->(m2:Method {app_key: key}) WHERE (m2.is_setter OR m2.is_getter) AND (cl)-[:CLASS_OWNS_METHOD]->(m2) RETURN m1.app_key as app_key";
            if (details) {
                query += ",m1.full_name as full_name,m2.full_name as gs_name";
            } else {
                query += ",count(m1) as IGS";
            }
            Result result = graphDatabaseService.execute(query);
            queryEngine.resultToCSV(result, "_IGS.csv");
        }
    }
}
