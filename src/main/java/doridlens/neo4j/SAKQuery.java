package doridlens.neo4j;

import net.sourceforge.jFuzzyLogic.FIS;
import net.sourceforge.jFuzzyLogic.FunctionBlock;
import org.neo4j.cypher.CypherException;
import org.neo4j.graphdb.Result;
import org.neo4j.graphdb.Transaction;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Author: MaoMorn
 * Date: 2020/1/2
 * Time: 9:47
 * Description:
 */
public class SAKQuery extends FuzzyQuery{
    protected static double high = 8.5;
    protected static double veryHigh = 13;

    private SAKQuery(QueryEngine queryEngine) {
        super(queryEngine);
        fclFile = "/fcl/SwissArmyKnife.fcl";
    }

    public static SAKQuery createSAKQuery(QueryEngine queryEngine) {
        return new SAKQuery(queryEngine);
    }

    public void execute(boolean details) throws CypherException, IOException {
        Result result;
        try (Transaction ignored = graphDatabaseService.beginTx()) {
            String query = "MATCH (cl:Class) WHERE EXISTS(cl.is_interface) AND cl.number_of_methods > " + veryHigh + " RETURN cl.app_key as app_key";
            if(details){
                query += ",cl.name as full_name";
            }else{
                query += ",count(cl) as SAK";
            }
            result = graphDatabaseService.execute(query);
            queryEngine.resultToCSV(result,"_SAK_NO_FUZZY.csv");
        }
    }

    public void executeFuzzy(boolean details) throws CypherException, IOException {
        Result result;
        try (Transaction ignored = graphDatabaseService.beginTx()) {
            String query = "MATCH (cl:Class) WHERE EXISTS(cl.is_interface) AND cl.number_of_methods > " + high + " RETURN cl.app_key as app_key,cl.number_of_methods as number_of_methods";
            if(details){
                query += ",cl.name as full_name";
            }
            result = graphDatabaseService.execute(query);
            List<String> columns = new ArrayList<>(result.columns());
            columns.add("fuzzy_value");
            int cc;
            List<Map> fuzzyResult = new ArrayList<>();
            File fcf = new File(fclFile);
            //We look if the file is in a directory otherwise we look inside the jar
            FIS fis;
            if(fcf.exists() && !fcf.isDirectory()){
                fis = FIS.load(fclFile, false);
            }else{
                fis = FIS.load(getClass().getResourceAsStream(fclFile),false);
            }
            FunctionBlock fb = fis.getFunctionBlock(null);
            while(result.hasNext()){
                HashMap res = new HashMap(result.next());
                cc = (int) res.get("number_of_methods");
                if(cc >= veryHigh){
                    res.put("fuzzy_value", 1);
                }else {
                    fb.setVariable("number_of_methods",cc);
                    fb.evaluate();
                    res.put("fuzzy_value", fb.getVariable("res").getValue());
                }
                fuzzyResult.add(res);
            }
            queryEngine.resultToCSV(fuzzyResult,columns,"_SAK.csv");
        }
    }
}

