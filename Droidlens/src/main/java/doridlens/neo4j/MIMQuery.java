package doridlens.neo4j;

import org.neo4j.cypher.CypherException;
import org.neo4j.graphdb.Result;
import org.neo4j.graphdb.Transaction;

import java.io.IOException;

/**
 * Author: MaoMorn
 * Date: 2020/1/2
 * Time: 9:45
 * Description:
 */
public class MIMQuery extends Query {

    private MIMQuery(QueryEngine queryEngine) {
        super(queryEngine);
    }

    public static MIMQuery createMIMQuery(QueryEngine queryEngine) {
        return new MIMQuery(queryEngine);
    }

    @Override
    public void execute(boolean details) throws CypherException, IOException {
        try (Transaction ignored = graphDatabaseService.beginTx()) {
            String query = "MATCH (m1:Method) WHERE m1.number_of_callers>0 AND NOT EXISTS(m1.is_static) AND NOT EXISTS(m1.is_override) AND NOT (m1)-[:USES]->(:Variable) AND NOT (m1)-[:CALLS]->(:ExternalMethod) AND NOT (m1)-[:CALLS]->(:Method) AND NOT EXISTS(m1.is_init)  RETURN m1.app_key as app_key";
            if(details){
                query += ",m1.full_name as full_name";
            }else{
                query += ",count(m1) as MIM";
            }
            Result result = graphDatabaseService.execute(query);
            queryEngine.resultToCSV(result, "_MIM.csv");
        }
    }
}
