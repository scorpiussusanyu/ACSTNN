package doridlens;

import doridlens.analyzer.Analyzer;
import doridlens.analyzer.SootAnalyzer;
import doridlens.neo4j.*;
import net.sourceforge.argparse4j.ArgumentParsers;
import net.sourceforge.argparse4j.inf.*;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.logging.Logger;

/**
 * Author: MaoMorn
 * Date: 2018/9/20
 * Time: 17:18
 * Description:
 */
public class Main {
    private final static Logger LOGGER = Logger.getLogger(Main.class.getName());

    public static void main(String[] args) {
        ArgumentParser parser = ArgumentParsers.newFor("doridlens").build();
        Subparsers subparsers = parser.addSubparsers().dest("sub_command");
        Subparser analyseParser = subparsers.addParser("analyse").help("Analyse an app");
        analyseParser.addArgument("apk").help("Path of the APK to analyze");
//        analyseParser.addArgument("-apk", "--apk").help("Path of the APK to analyze");
        analyseParser.addArgument("-a", "--androidJars").required(true).help("Path to android platforms jars");
        analyseParser.addArgument("-db", "--database").required(true).help("Path to neo4J Database folder");
        analyseParser.addArgument("-n", "--name").required(true).help("Name of the application");
        analyseParser.addArgument("-p", "--package").required(true).help("Application main package");
        analyseParser.addArgument("-omp", "--onlyMainPackage").type(Boolean.class).setDefault(false).help("Analyze only the main package of the application");

        Subparser queryParser = subparsers.addParser("query").help("Query the database");
        queryParser.addArgument("-db", "--database").required(true).help("Path to neo4J Database folder");
        queryParser.addArgument("-r", "--request").help("Request to execute");
        queryParser.addArgument("-c", "--csv").help("path to register csv files").setDefault("");
        queryParser.addArgument("-dk", "--delKey").help("key to delete");
        queryParser.addArgument("-dp", "--delPackage").help("Package of the applications to delete");
        queryParser.addArgument("-d", "--details").type(Boolean.class).setDefault(false).help("Show the concerned doridlens.entity in the results");
        try {
            Namespace res = parser.parseArgs(args);
            if (res.getString("sub_command").equals("analyse")) {
                runAnalysis(res);
            } else if (res.getString("sub_command").equals("query")) {
                queryMode(res);
            }
        } catch (ArgumentParserException e) {
            analyseParser.handleError(e);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void runAnalysis(Namespace arg) throws Exception {
        System.out.println("Collecting doridlens.metrics");
        Analyzer analyzer = new SootAnalyzer(arg.getString("apk"), arg.getString("androidJars"),
                arg.getString("name"), arg.getString("package"), arg.getBoolean("onlyMainPackage"));
        analyzer.init();
        analyzer.runAnalysis();
        System.out.println("Saving into database " + arg.getString("database"));
        ModelToGraph modelToGraph = new ModelToGraph(arg.getString("database"));
        modelToGraph.insertApp(analyzer.getDoridlensApp());
        System.out.println("Done");
    }

    public static void queryMode(Namespace arg) throws Exception {
        System.out.println("Executing Queries");
        QueryEngine queryEngine = new QueryEngine(arg.getString("database"));
        String request = arg.get("request");
        Boolean details = arg.get("details");
        String csvDate = new SimpleDateFormat("yyyy_MM_dd_HH_mm_ss").format(new Date());
        String csvPrefix = arg.getString("csv") + "\\" + csvDate;
        System.out.println("Resulting csv file name will start with prefix " + csvPrefix);
        queryEngine.setCsvPrefix(csvPrefix);
        switch (request) {
            case "ARGB8888":
                ARGB8888Query.createARGB8888Query(queryEngine).execute(details);
            case "MIM":
                MIMQuery.createMIMQuery(queryEngine).execute(details);
                break;
            case "IGS":
                IGSQuery.createIGSQuery(queryEngine).execute(details);
                break;
            case "LIC":
                LICQuery.createLICQuery(queryEngine).execute(details);
                break;
            case "NLMR":
                NLMRQuery.createNLMRQuery(queryEngine).execute(details);
                break;
            case "CC":
                CCQuery.createCCQuery(queryEngine).executeFuzzy(details);
                break;
            case "LM":
                LMQuery.createLMQuery(queryEngine).executeFuzzy(details);
                break;
            case "SAK":
                SAKQuery.createSAKQuery(queryEngine).executeFuzzy(details);
                break;
            case "BLOB":
                BLOBQuery.createBLOBQuery(queryEngine).executeFuzzy(details);
                break;
            case "OVERDRAW":
                OverdrawQuery.createOverdrawQuery(queryEngine).execute(details);
                break;
            case "HSS":
                HeavyServiceStartQuery.createHeavyServiceStartQuery(queryEngine).executeFuzzy(details);
                break;
            case "HBR":
                HeavyBroadcastReceiverQuery.createHeavyBroadcastReceiverQuery(queryEngine).executeFuzzy(details);
                break;
            case "HAS":
                HeavyAsyncTaskStepsQuery.createHeavyAsyncTaskStepsQuery(queryEngine).executeFuzzy(details);
                break;
            case "THI":
                TrackingHardwareIdQuery.createTrackingHardwareIdQuery(queryEngine).execute(details);
                break;
            case "ALLHEAVY":
                HeavyServiceStartQuery.createHeavyServiceStartQuery(queryEngine).executeFuzzy(details);
                HeavyBroadcastReceiverQuery.createHeavyBroadcastReceiverQuery(queryEngine).executeFuzzy(details);
                HeavyAsyncTaskStepsQuery.createHeavyAsyncTaskStepsQuery(queryEngine).executeFuzzy(details);
                break;
            case "ANALYZED":
                queryEngine.AnalyzedAppQuery();
                break;
            case "DELETE":
                queryEngine.deleteQuery(arg.getString("delKey"));
                break;
            case "DELETEAPP":
                if (arg.get("delKey") != null) {
                    queryEngine.deleteEntireApp(arg.getString("delKey"));
                } else {
                    queryEngine.deleteEntireAppFromPackage(arg.getString("delPackage"));
                }
                break;
            case "STATS":
                QuartileCalculator quartileCalculator = new QuartileCalculator(queryEngine);
                quartileCalculator.calculateClassComplexityQuartile();
                quartileCalculator.calculateLackofCohesionInMethodsQuartile();
                quartileCalculator.calculateNumberOfAttributesQuartile();
                quartileCalculator.calculateNumberOfImplementedInterfacesQuartile();
                quartileCalculator.calculateNumberOfMethodsQuartile();
                quartileCalculator.calculateNumberofInstructionsQuartile();
                quartileCalculator.calculateCyclomaticComplexityQuartile();
                quartileCalculator.calculateNumberOfMethodsForInterfacesQuartile();
                break;
            case "ALLLCOM":
                queryEngine.getAllLCOM();
                break;
            case "ALLCYCLO":
                queryEngine.getAllCyclomaticComplexity();
                break;
            case "ALLCC":
                queryEngine.getAllClassComplexity();
                break;
            case "ALLNUMMETHODS":
                queryEngine.getAllNumberOfMethods();
                break;
            case "COUNTVAR":
                queryEngine.countVariables();
                break;
            case "COUNTINNER":
                queryEngine.countInnerClasses();
                break;
            case "COUNTASYNC":
                queryEngine.countAsyncClasses();
                break;
            case "COUNTVIEWS":
                queryEngine.countViews();
                break;
            case "NONFUZZY":
                ARGB8888Query.createARGB8888Query(queryEngine).execute(details);
                IGSQuery.createIGSQuery(queryEngine).execute(details);
                MIMQuery.createMIMQuery(queryEngine).execute(details);
                LICQuery.createLICQuery(queryEngine).execute(details);
                NLMRQuery.createNLMRQuery(queryEngine).execute(details);
                OverdrawQuery.createOverdrawQuery(queryEngine).execute(details);
                UnsuitedLRUCacheSizeQuery.createUnsuitedLRUCacheSizeQuery(queryEngine).execute(details);
                InitOnDrawQuery.createInitOnDrawQuery(queryEngine).execute(details);
                UnsupportedHardwareAccelerationQuery.createUnsupportedHardwareAccelerationQuery(queryEngine).execute(details);
                HashMapUsageQuery.createHashMapUsageQuery(queryEngine).execute(details);
                InvalidateWithoutRectQuery.createInvalidateWithoutRectQuery(queryEngine).execute(details);
                break;
            case "FUZZY":
                CCQuery.createCCQuery(queryEngine).executeFuzzy(details);
                LMQuery.createLMQuery(queryEngine).executeFuzzy(details);
                SAKQuery.createSAKQuery(queryEngine).executeFuzzy(details);
                BLOBQuery.createBLOBQuery(queryEngine).executeFuzzy(details);
                HeavyServiceStartQuery.createHeavyServiceStartQuery(queryEngine).executeFuzzy(details);
                HeavyBroadcastReceiverQuery.createHeavyBroadcastReceiverQuery(queryEngine).executeFuzzy(details);
                HeavyAsyncTaskStepsQuery.createHeavyAsyncTaskStepsQuery(queryEngine).executeFuzzy(details);
                break;
            case "ALLAP":
                ARGB8888Query.createARGB8888Query(queryEngine).execute(details);
                CCQuery.createCCQuery(queryEngine).executeFuzzy(details);
                LMQuery.createLMQuery(queryEngine).executeFuzzy(details);
                SAKQuery.createSAKQuery(queryEngine).executeFuzzy(details);
                BLOBQuery.createBLOBQuery(queryEngine).executeFuzzy(details);
                MIMQuery.createMIMQuery(queryEngine).execute(details);
                IGSQuery.createIGSQuery(queryEngine).execute(details);
                LICQuery.createLICQuery(queryEngine).execute(details);
                NLMRQuery.createNLMRQuery(queryEngine).execute(details);
                OverdrawQuery.createOverdrawQuery(queryEngine).execute(details);
                HeavyServiceStartQuery.createHeavyServiceStartQuery(queryEngine).executeFuzzy(details);
                HeavyBroadcastReceiverQuery.createHeavyBroadcastReceiverQuery(queryEngine).executeFuzzy(details);
                HeavyAsyncTaskStepsQuery.createHeavyAsyncTaskStepsQuery(queryEngine).executeFuzzy(details);
                UnsuitedLRUCacheSizeQuery.createUnsuitedLRUCacheSizeQuery(queryEngine).execute(details);
                InitOnDrawQuery.createInitOnDrawQuery(queryEngine).execute(details);
                UnsupportedHardwareAccelerationQuery.createUnsupportedHardwareAccelerationQuery(queryEngine).execute(details);
                HashMapUsageQuery.createHashMapUsageQuery(queryEngine).execute(details);
                InvalidateWithoutRectQuery.createInvalidateWithoutRectQuery(queryEngine).execute(details);
                TrackingHardwareIdQuery.createTrackingHardwareIdQuery(queryEngine).execute(details);
                break;
            case "FORCENOFUZZY":
                CCQuery.createCCQuery(queryEngine).execute(details);
                LMQuery.createLMQuery(queryEngine).execute(details);
                SAKQuery.createSAKQuery(queryEngine).execute(details);
                BLOBQuery.createBLOBQuery(queryEngine).execute(details);
                HeavyServiceStartQuery.createHeavyServiceStartQuery(queryEngine).execute(details);
                HeavyBroadcastReceiverQuery.createHeavyBroadcastReceiverQuery(queryEngine).execute(details);
                HeavyAsyncTaskStepsQuery.createHeavyAsyncTaskStepsQuery(queryEngine).execute(details);
                break;
            default:
                System.out.println("Executing custom request");
                queryEngine.executeRequest(request);
        }
        queryEngine.shutDown();
        System.out.println("Done");
    }
}
