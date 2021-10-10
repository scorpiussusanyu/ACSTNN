package doridlens.neo4j;

import doridlens.entity.*;
import org.neo4j.graphdb.GraphDatabaseService;
import org.neo4j.graphdb.Node;
import org.neo4j.graphdb.Transaction;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

/**
 * Author: MaoMorn
 * Date: 2020/1/2
 * Time: 9:45
 * Description:
 */
public class ModelToGraph {
    private GraphDatabaseService graphDatabaseService;
    private DatabaseManager databaseManager;

    private Map<Entity, Node> methodNodeMap;
    private Map<DoridlensClass, Node> classNodeMap;
    private Map<DoridlensVariable, Node> variableNodeMap;

    public ModelToGraph(String DatabasePath) {
        this.databaseManager = new DatabaseManager(DatabasePath);
        databaseManager.start();
        this.graphDatabaseService = databaseManager.getGraphDatabaseService();
        methodNodeMap = new HashMap<>();
        classNodeMap = new HashMap<>();
        variableNodeMap = new HashMap<>();
        IndexManager indexManager = new IndexManager(graphDatabaseService);
        indexManager.createIndex();
    }

    public Node insertApp(DoridlensApp doridlensApp) {
        Node appNode;
        try (Transaction tx = graphDatabaseService.beginTx()) {
            appNode = graphDatabaseService.createNode(Labels.App);
            appNode.setProperty("name", doridlensApp.getName());
            Date date = new Date();
            SimpleDateFormat simpleFormat = new SimpleDateFormat("yyyy-mm-dd hh:mm:ss.S");
            appNode.setProperty("date_analysis", simpleFormat.format(date));
            for (DoridlensClass doridlensClass : doridlensApp.getDoridlensClasses()) {
                appNode.createRelationshipTo(insertClass(doridlensClass), RelationTypes.APP_OWNS_CLASS);
            }
            for (DoridlensExternalClass doridlensExternalClass : doridlensApp.getDoridlensExternalClasses()) {
                insertExternalClass(doridlensExternalClass);
            }
            HashMap<String, Object> metrics = doridlensApp.getMetrics();
            for (String key : metrics.keySet()) {
                appNode.setProperty(key, metrics.get(key));
            }
            tx.success();
        }
        try (Transaction tx = graphDatabaseService.beginTx()) {
            createHierarchy(doridlensApp);
            createCallGraph(doridlensApp);
            tx.success();
        }
        return appNode;
    }

    public Node insertClass(DoridlensClass doridlensClass) {
        Node classNode = graphDatabaseService.createNode(Labels.Class);
        classNodeMap.put(doridlensClass, classNode);
        classNode.setProperty("name", doridlensClass.getName());
        classNode.setProperty("modifier", doridlensClass.getModifier().toString().toLowerCase());
        if (doridlensClass.getParentName() != null) {
            classNode.setProperty("parent_name", doridlensClass.getParentName());
        }
        for (DoridlensVariable doridlensVariable : doridlensClass.getDoridlensVariables()) {
            classNode.createRelationshipTo(insertVariable(doridlensVariable), RelationTypes.CLASS_OWNS_VARIABLE);
        }
        for (DoridlensMethod doridlensMethod : doridlensClass.getDoridlensMethods()) {
            classNode.createRelationshipTo(insertMethod(doridlensMethod), RelationTypes.CLASS_OWNS_METHOD);
        }
        HashMap<String, Object> metrics = doridlensClass.getMetrics();
        for (String key : metrics.keySet()) {
            classNode.setProperty(key, metrics.get(key));
        }
        return classNode;
    }

    public Node insertExternalClass(DoridlensExternalClass doridlensClass) {
        Node classNode = graphDatabaseService.createNode(Labels.ExternalClass);
        classNode.setProperty("name", doridlensClass.getName());
        if (doridlensClass.getParentName() != null) {
            classNode.setProperty("parent_name", doridlensClass.getParentName());
        }
        for (DoridlensExternalMethod doridlensExternalMethod : doridlensClass.getDoridlensExternalMethods()) {
            classNode.createRelationshipTo(insertExternalMethod(doridlensExternalMethod), RelationTypes.CLASS_OWNS_METHOD);
        }
        HashMap<String, Object> metrics = doridlensClass.getMetrics();
        for (String key : metrics.keySet()) {
            classNode.setProperty(key, metrics.get(key));
        }
        return classNode;
    }

    public Node insertVariable(DoridlensVariable doridlensVariable) {
        Node variableNode = graphDatabaseService.createNode(Labels.Variable);
        variableNodeMap.put(doridlensVariable, variableNode);
        variableNode.setProperty("name", doridlensVariable.getName());
        variableNode.setProperty("modifier", doridlensVariable.getModifier().toString().toLowerCase());
        variableNode.setProperty("type", doridlensVariable.getType());
        HashMap<String, Object> metrics = doridlensVariable.getMetrics();
        for (String key : metrics.keySet()) {
            variableNode.setProperty(key, metrics.get(key));
        }
        return variableNode;
    }

    public Node insertMethod(DoridlensMethod doridlensMethod) {
        Node methodNode = graphDatabaseService.createNode(Labels.Method);
        methodNodeMap.put(doridlensMethod, methodNode);
        methodNode.setProperty("name", doridlensMethod.getName());
        methodNode.setProperty("modifier", doridlensMethod.getModifier().toString().toLowerCase());
        methodNode.setProperty("full_name", doridlensMethod.toString());
        methodNode.setProperty("return_type", doridlensMethod.getReturnType());
        HashMap<String, Object> metrics = doridlensMethod.getMetrics();
        for (String key : metrics.keySet()) {
            methodNode.setProperty(key, metrics.get(key));
        }
        for (DoridlensVariable doridlensVariable : doridlensMethod.getUsedVariables()) {
            methodNode.createRelationshipTo(variableNodeMap.get(doridlensVariable), RelationTypes.USES);
        }
        for (DoridlensArgument arg : doridlensMethod.getArguments()) {
            methodNode.createRelationshipTo(insertArgument(arg), RelationTypes.METHOD_OWNS_ARGUMENT);
        }
        return methodNode;
    }

    public Node insertExternalMethod(DoridlensExternalMethod doridlensMethod) {
        Node methodNode = graphDatabaseService.createNode(Labels.ExternalMethod);
        methodNodeMap.put(doridlensMethod, methodNode);
        methodNode.setProperty("name", doridlensMethod.getName());
        methodNode.setProperty("full_name", doridlensMethod.toString());
        methodNode.setProperty("return_type", doridlensMethod.getReturnType());
        HashMap<String, Object> metrics = doridlensMethod.getMetrics();
        for (String key : metrics.keySet()) {
            methodNode.setProperty(key, metrics.get(key));
        }
        for (DoridlensExternalArgument arg : doridlensMethod.getDoridlensExternalArguments()) {
            methodNode.createRelationshipTo(insertExternalArgument(arg), RelationTypes.METHOD_OWNS_ARGUMENT);
        }
        return methodNode;
    }

    public Node insertArgument(DoridlensArgument doridlensArgument) {
        Node argNode = graphDatabaseService.createNode(Labels.Argument);
        argNode.setProperty("name", doridlensArgument.getName());
        argNode.setProperty("position", doridlensArgument.getPosition());
        return argNode;
    }

    public Node insertExternalArgument(DoridlensExternalArgument doridlensExternalArgument) {
        Node argNode = graphDatabaseService.createNode(Labels.ExternalArgument);
        argNode.setProperty("name", doridlensExternalArgument.getName());
        argNode.setProperty("position", doridlensExternalArgument.getPosition());
        HashMap<String, Object> metrics = doridlensExternalArgument.getMetrics();
        for (String key : metrics.keySet()) {
            argNode.setProperty(key, metrics.get(key));
        }
        return argNode;
    }

    public void createHierarchy(DoridlensApp doridlensApp) {
        for (DoridlensClass doridlensClass : doridlensApp.getDoridlensClasses()) {
            DoridlensClass parent = doridlensClass.getParent();
            if (parent != null) {
                classNodeMap.get(doridlensClass).createRelationshipTo(classNodeMap.get(parent), RelationTypes.EXTENDS);
            }
            for (DoridlensClass pInterface : doridlensClass.getInterfaces()) {
                classNodeMap.get(doridlensClass).createRelationshipTo(classNodeMap.get(pInterface), RelationTypes.IMPLEMENTS);
            }
        }
    }

    public void createCallGraph(DoridlensApp doridlensApp) {
        for (DoridlensClass doridlensClass : doridlensApp.getDoridlensClasses()) {
            for (DoridlensMethod doridlensMethod : doridlensClass.getDoridlensMethods()) {
                for (Entity calledMethod : doridlensMethod.getCalledMethods()) {
                    methodNodeMap.get(doridlensMethod).createRelationshipTo(methodNodeMap.get(calledMethod), RelationTypes.CALLS);
                }
            }
        }
    }
}

