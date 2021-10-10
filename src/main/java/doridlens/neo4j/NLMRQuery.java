package doridlens.neo4j;

import org.neo4j.cypher.CypherException;
import org.neo4j.graphdb.Result;
import org.neo4j.graphdb.Transaction;

import java.io.IOException;

/**
 * Author: MaoMorn
 * Date: 2020/1/2
 * Time: 9:46
 * Description:
 */
public class NLMRQuery extends Query {

    private NLMRQuery(QueryEngine queryEngine) {
        super(queryEngine);
    }

    public static NLMRQuery createNLMRQuery(QueryEngine queryEngine) {
        return new NLMRQuery(queryEngine);
    }

    @Override
    public void execute(boolean details) throws CypherException, IOException {
        try (Transaction ignored = graphDatabaseService.beginTx()) {
            String query = "MATCH (cl:Class) WHERE EXISTS(cl.is_activity) AND NOT (cl:Class)-[:CLASS_OWNS_METHOD]->(:Method { name: 'onLowMemory' }) AND NOT (cl)-[:EXTENDS]->(:Class) RETURN cl.app_key as app_key";
            if(details){
                query += ",cl.name as full_name";
            }else{
                query += ",count(cl) as NLMR";
            }
            Result result = graphDatabaseService.execute(query);
            queryEngine.resultToCSV(result, "_NLMR.csv");
        }
    }
}
