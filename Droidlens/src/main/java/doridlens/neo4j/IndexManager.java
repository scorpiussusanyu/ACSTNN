package doridlens.neo4j;

import org.neo4j.graphdb.GraphDatabaseService;
import org.neo4j.graphdb.Transaction;
import org.neo4j.graphdb.schema.Schema;

/**
 * Author: MaoMorn
 * Date: 2020/1/2
 * Time: 9:42
 * Description:
 */
public class IndexManager {
    private GraphDatabaseService graphDatabaseService;

    public IndexManager(GraphDatabaseService graphDatabaseService) {
        this.graphDatabaseService = graphDatabaseService;
    }

    public void createIndex() {
        try (Transaction tx = graphDatabaseService.beginTx()) {
            Schema schema = graphDatabaseService.schema();
            if (schema.getIndexes(Labels.Variable).iterator().hasNext()) {
                schema.indexFor(Labels.Variable)
                        .on("app_key")
                        .create();
            }
            if (schema.getIndexes(Labels.Method).iterator().hasNext()) {
                schema.indexFor(Labels.Method)
                        .on("app_key")
                        .create();
                schema.indexFor(Labels.Method)
                        .on("is_static")
                        .create();
            }
            if (schema.getIndexes(Labels.Argument).iterator().hasNext()) {
                schema.indexFor(Labels.Argument)
                        .on("app_key")
                        .create();
                schema.indexFor(Labels.Argument)
                        .on("app_key")
                        .create();
            }
            if (schema.getIndexes(Labels.ExternalClass).iterator().hasNext()) {
                schema.indexFor(Labels.ExternalClass)
                        .on("app_key")
                        .create();
            }
            if (schema.getIndexes(Labels.ExternalMethod).iterator().hasNext()) {
                schema.indexFor(Labels.ExternalMethod)
                        .on("app_key")
                        .create();
            }
            tx.success();
        }
        try (Transaction tx = graphDatabaseService.beginTx()) {
            org.neo4j.graphdb.index.IndexManager index = graphDatabaseService.index();
            if (!index.existsForRelationships("calls")) {
                index.forRelationships("calls");
            }
            tx.success();
        }
    }
}

