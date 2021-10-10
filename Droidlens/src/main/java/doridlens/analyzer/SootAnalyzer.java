package doridlens.analyzer;

import doridlens.entity.*;
import doridlens.metrics.*;
import soot.*;
import soot.grimp.GrimpBody;
import soot.grimp.internal.GAssignStmt;
import soot.grimp.internal.GLookupSwitchStmt;
import soot.grimp.internal.GRValueBox;
import soot.jimple.FieldRef;
import soot.jimple.StaticFieldRef;
import soot.jimple.toolkits.callgraph.CallGraph;
import soot.jimple.toolkits.callgraph.Edge;
import soot.options.Options;
import soot.util.Chain;

import java.io.File;
import java.io.OutputStream;
import java.io.PrintStream;
import java.util.*;
import java.util.logging.Logger;

/**
 * Author: MaoMorn
 * Date: 2020/1/2
 * Time: 9:16
 * Description:
 */
public class SootAnalyzer extends Analyzer {
    private final static Logger LOGGER = Logger.getLogger(SootAnalyzer.class.getName());
    private String apk;
    private String androidJAR;
    private DoridlensApp doridlensApp;
    private Map<SootClass, DoridlensClass> classMap;
    private Map<SootClass, DoridlensExternalClass> externalClassMap;
    private Map<SootMethod, DoridlensExternalMethod> externalMethodMap;
    private Map<SootMethod, DoridlensMethod> methodMap;
    int argb8888Count = 0, activityCount = 0, innerCount = 0, varCount = 0, asyncCount = 0, serviceCount = 0, viewCount = 0, interfaceCount = 0, abstractCount = 0, broadcastReceiverCount = 0, contentProviderCount = 0;
    private String rClass;
    private String buildConfigClass;
    private String pack;
    private boolean mainPackageOnly = false;

    public SootAnalyzer(String apk, String androidJAR, String name, String pack, boolean mainPackageOnly) {
        this.apk = apk;
        this.androidJAR = androidJAR;
        this.pack = pack;
        this.doridlensApp = DoridlensApp.createDoridlensApp(name, pack);
        this.rClass = pack.concat(".R");
        this.buildConfigClass = pack.concat(".BuildConfig");
        this.classMap = new HashMap<>();
        this.externalClassMap = new HashMap<>();
        this.externalMethodMap = new HashMap<>();
        this.methodMap = new HashMap<>();
        this.mainPackageOnly = mainPackageOnly;
    }

    @Override
    public void init() {
        //Hack to prevent soot to print on System.out
        PrintStream originalStream = System.out;
        System.setOut(new PrintStream(new OutputStream() {
            public void write(int b) {
                // NO-OP
            }
        }));
        G.reset();
        Options.v().set_verbose(false);
        //Options.v().set_keep_line_number(true);
        //Path to android-sdk-platforms
        Options.v().set_android_jars(androidJAR);
        //Options.v().set_soot_classpath("/home/geoffrey/These/decompiler/android-platforms/android-14/android.jar");
        //prefer Android APK files
        Options.v().set_src_prec(Options.src_prec_apk);
        //Options.v().set_src_prec(Options.src_prec_java);
        // Allow phantom references
        Options.v().set_allow_phantom_refs(true);
        //Set path to APK
        Options.v().set_process_dir(Collections.singletonList(apk));
        //Options.v().set_process_dir(Collections.singletonList("/home/geoffrey/These/LotOfAntiPatternsApplication/app/src/main/java"));
        Options.v().set_whole_program(true);
        Options.v().set_output_format(Options.output_format_grimple);
        //Options.v().set_output_dir("/home/geoffrey/These/decompiler/out");
        //Get directly the home directory and work on it
        Options.v().set_output_dir(System.getProperty("user.home") + File.separator + "/These/decompiler/out");
        //Options.v().set_soot_classpath();
        PhaseOptions.v().setPhaseOption("gop", "enabled:true");
        System.setOut(originalStream);
        //Options.v().set_soot_classpath(Scene.v().getAndroidJarPath(androidJAR,apk));
        List<String> excludeList = new LinkedList<String>();
        excludeList.add("java.");
        excludeList.add("sun.misc.");
        excludeList.add("android.");
        excludeList.add("org.apache.");
        excludeList.add("soot.");
        excludeList.add("javax.servlet.");
        Options.v().set_exclude(excludeList);
        //Options.v().set_no_bodies_for_excluded(true);
        //Options.v().setPhaseOption("cg","verbose:true");
        //Options.v().setPhaseOption("cg.cha", "on");
        Scene.v().loadNecessaryClasses();
    }

    @Override
    public void runAnalysis() {
        collectClassesMetrics();
        collectAppMetrics();
        PackManager.v().getPack("gop").add(new Transform("gop.myInstrumenter", new BodyTransformer() {

            @Override
            protected void internalTransform(final Body body, String phaseName, @SuppressWarnings("rawtypes") Map options) {
                collectMethodsMetrics(body.getMethod());
            }


        }));
        PackManager.v().runPacks();
        computeMetrics();
        collectCallGraphMetrics();
        //PackManager.v().writeOutput();
    }

    private void collectCallGraphMetrics() {
        for (Map.Entry<SootMethod, DoridlensMethod> entry : methodMap.entrySet()) {
            collectMethodMetricsFromCallGraph(entry.getValue(), entry.getKey());
        }
    }

    @Override
    public DoridlensApp getDoridlensApp() {
        return doridlensApp;
    }

    /**
     * Should be called after all classes have been processed once
     */
    public void collectAppMetrics() {
        AppMetrics.createNumberOfClasses(this.doridlensApp, classMap.size());
        AppMetrics.createNumberOfActivities(this.doridlensApp, activityCount);
        AppMetrics.createNumberOfServices(this.doridlensApp, serviceCount);
        AppMetrics.createNumberOfInnerClasses(this.doridlensApp, innerCount);
        AppMetrics.createNumberOfAsyncTasks(this.doridlensApp, asyncCount);
        AppMetrics.createNumberOfViews(this.doridlensApp, viewCount);
        AppMetrics.createNumberOfVariables(this.doridlensApp, varCount);
        AppMetrics.createNumberOfInterfaces(this.doridlensApp, interfaceCount);
        AppMetrics.createNumberOfAbstractClasses(this.doridlensApp, abstractCount);
        AppMetrics.createNumberOfBroadcastReceivers(this.doridlensApp, broadcastReceiverCount);
        AppMetrics.createNumberOfContentProviders(this.doridlensApp, contentProviderCount);
    }

    public void collectClassesMetrics() {
        Chain<SootClass> sootClasses = Scene.v().getApplicationClasses();
        for (SootClass sootClass : sootClasses) {
            //Excluding R And BuildConfig class from the analysis
            String rsubClassStart = rClass + "$";
            String name = sootClass.getName();
            String packs = pack.concat(".");
            if (name.equals(rClass) || name.startsWith(rsubClassStart) || name.equals(buildConfigClass)) {
                //sootClass.setLibraryClass();
            } else if (!mainPackageOnly || name.startsWith(packs)) {
                collectClassMetrics(sootClass);
            }
        }
        // Now that all classes have been processed at least once (and the map filled) we can process NOC
        for (SootClass sootClass : sootClasses) {
            if (sootClass.hasSuperclass()) {
                SootClass superClass = sootClass.getSuperclass();
                DoridlensClass doridlensClass = classMap.get(superClass);
                if (doridlensClass != null) classMap.get(superClass).addChildren();
            }
        }
    }

    /**
     * Should be called last
     */
    public void computeMetrics() {
        computeInheritance();
        computeInterface();
        for (DoridlensClass doridlensClass : doridlensApp.getDoridlensClasses()) {
            // Create complexity with the final value
            ClassMetrics.createClassComplexity(doridlensClass);
            // Create NOC with the final value
            ClassMetrics.createNumberOfChildren(doridlensClass);
            // CBO with final value
            ClassMetrics.createCouplingBetweenObjects(doridlensClass);
            //LCOM
            ClassMetrics.createLackofCohesionInMethods(doridlensClass);
            // Compute the NPath complexity, per class
            ClassMetrics.createNPathComplexity(doridlensClass);
        }
        CommonMetrics.createNumberOfMethods(doridlensApp, methodMap.size());
    }

    /**
     * Should be called after all classes have been processed once
     */
    public void collectMethodsMetrics(SootMethod sootMethod) {
        SootClass sootClass = sootMethod.getDeclaringClass();
        DoridlensClass doridlensClass = classMap.get(sootClass);
        if (doridlensClass == null) {
            //Should be R or external classes
            //LOGGER.warning("Class not analyzed : "+ sootClass);
            sootClass.setLibraryClass();
            return;
            /*
            doridlensClass = DoridlensClass.createDoridlensClass(sootClass.getName(), this.doridlensApp);
            classMap.put(sootClass, doridlensClass);
            */
        }
        DoridlensModifiers modifiers = DoridlensModifiers.PRIVATE;
        if (sootMethod.isPublic()) {
            modifiers = DoridlensModifiers.PUBLIC;
        } else if (sootMethod.isProtected()) {
            modifiers = DoridlensModifiers.PROTECTED;
        }

        DoridlensMethod doridlensMethod = DoridlensMethod.createDoridlensMethod(sootMethod.getName(), modifiers, sootMethod.getReturnType().toString(), doridlensClass);
        methodMap.put(sootMethod, doridlensMethod);
        if (sootMethod.isStatic()) {
            CommonMetrics.createIsStatic(doridlensMethod, true);
        }
        if (sootMethod.isFinal()) {
            CommonMetrics.createIsFinal(doridlensMethod, true);
        }
        if (sootMethod.isSynchronized()) {
            MethodMetrics.createIsSynchronized(doridlensMethod, true);
        }
        if (sootMethod.isAbstract()) {
            CommonMetrics.createIsAbstract(doridlensMethod, true);
        }
        MethodMetrics.createNumberOfParameters(doridlensMethod, sootMethod.getParameterCount());
        if (sootMethod.hasActiveBody()) {
            //Args
            int i = 0;
            for (Type type : sootMethod.getParameterTypes()) {
                i++;
                DoridlensArgument.createDoridlensArgument(type.toString(), i, doridlensMethod);
            }
            GrimpBody activeBody = (GrimpBody) sootMethod.getActiveBody();
            // Number of lines is the number of Units - number of Parameter - 1 (function name)
            int nbOfLines = activeBody.getUnits().size() - sootMethod.getParameterCount() - 1;
            MethodMetrics.createNumberOfDeclaredLocals(doridlensMethod, activeBody.getLocals().size());
            MethodMetrics.createNumberOfInstructions(doridlensMethod, nbOfLines);
            // Cyclomatic complexity & Lack of Cohesion methods
            int nbOfBranches = 1;
            DoridlensVariable doridlensVariable = null;
            for (Unit sootUnit : activeBody.getUnits()) {
                //LCOM

                List<ValueBox> boxes = sootUnit.getUseAndDefBoxes();
                for (ValueBox valueBox : boxes) {
                    Value value = valueBox.getValue();
                    if (value instanceof FieldRef) {
                        SootFieldRef field = ((FieldRef) value).getFieldRef();
                        if (field.declaringClass() == sootClass) {
                            doridlensVariable = doridlensClass.findVariable(field.name());
                            //If we don't find the field it's inherited and thus not used for LCOM2
                            if (doridlensVariable != null) {
                                doridlensMethod.useVariable(doridlensVariable);
                            }
                        }
                    }
                }
                //Cyclomatic complexity
                if (sootUnit.branches()) {
                    if (sootUnit.fallsThrough()) nbOfBranches++;
                    else if (sootUnit instanceof GLookupSwitchStmt)
                        nbOfBranches += ((GLookupSwitchStmt) sootUnit).getLookupValues().size();
                }
            }
            MethodMetrics.createCyclomaticComplexity(doridlensMethod, nbOfBranches);
            if (isInit(sootMethod)) {
                MethodMetrics.createIsInit(doridlensMethod, true);
            } else {
                if (isOverride(sootMethod)) {
                    MethodMetrics.createIsOverride(doridlensMethod, true);
                }
                //Is it a probable getter/setter ?
                if (nbOfBranches == 1 && doridlensMethod.getUsedVariables().size() == 1 && sootMethod.getExceptions().size() == 0) {
                    doridlensVariable = doridlensMethod.getUsedVariables().iterator().next();
                    int parameterCount = sootMethod.getParameterCount();
                    int unitSize = sootMethod.getActiveBody().getUnits().size();
                    String returnType = doridlensMethod.getReturnType();
                    if (parameterCount == 1 && unitSize <= 4 && returnType.equals("void")) {
                        MethodMetrics.createIsSetter(doridlensMethod, true);
                    } else if (parameterCount == 0 && unitSize <= 3 && returnType.equals(doridlensVariable.getType())) {
                        MethodMetrics.createIsGetter(doridlensMethod, true);
                    }
                }
            }
        } else {
            //LOGGER.info("No body for "+doridlensMethod);
        }
    }

    private boolean isInit(SootMethod sootMethod) {
        String name = sootMethod.getName();
        return name.equals("<init>") || name.equals("<clinit>");
    }

    private void collectMethodMetricsFromCallGraph(DoridlensMethod doridlensMethod, SootMethod sootMethod) {
        CallGraph callGraph = Scene.v().getCallGraph();
        int edgeOutCount = 0, edgeIntoCount = 0;
        Iterator<Edge> edgeOutIterator = callGraph.edgesOutOf(sootMethod);
        Iterator<Edge> edgeIntoIterator = callGraph.edgesInto(sootMethod);
        callGraph = null;
        DoridlensClass currentClass = doridlensMethod.getDoridlensClass();
        while (edgeOutIterator.hasNext()) {
            Edge e = edgeOutIterator.next();
            SootMethod target = e.tgt();
            DoridlensMethod targetMethod = methodMap.get(target);
            //In the case we are calling an external method (sdk or library)
            //if(targetMethod == null && !isInit(e.tgt())){
            if (targetMethod == null) {
                DoridlensExternalMethod externalTgtMethod = externalMethodMap.get(target);
                if (externalTgtMethod == null) {
                    DoridlensExternalClass doridlensExternalClass = externalClassMap.get(target.getDeclaringClass());
                    if (doridlensExternalClass == null) {
                        doridlensExternalClass = DoridlensExternalClass.createDoridlensExternalClass(target.getDeclaringClass().getName(), doridlensApp);
                        externalClassMap.put(target.getDeclaringClass(), doridlensExternalClass);
                    }
                    externalTgtMethod = DoridlensExternalMethod.createDoridlensExternalMethod(target.getName(), target.getReturnType().toString(), doridlensExternalClass);
                    int i = 0;
                    for (Type type : target.getParameterTypes()) {
                        i++;
                        DoridlensExternalArgument doridlensExternalArgument = DoridlensExternalArgument.createDoridlensExternalArgument(type.toString(), i, externalTgtMethod);
                        if (doridlensExternalArgument.getName() == "android.graphics.Bitmap$Config") {
                            for (Unit unitChain : ((SootMethod) e.getSrc()).getActiveBody().getUnits()) {
                                try {
                                    String nameOfStaticFieldRef = ((StaticFieldRef) ((GRValueBox) ((GAssignStmt) unitChain).getRightOpBox()).getValue()).getFieldRef().name();
                                    if (nameOfStaticFieldRef.equals("ARGB_8888")) {
                                        argb8888Count++;
                                        ArgumentMetrics.createIsARGB8888(doridlensExternalArgument, true);
                                    }
                                } catch (Exception new_exception) {

                                }
                            }
                        }
                    }
                    externalMethodMap.put(target, externalTgtMethod);
                }
                doridlensMethod.callMethod(externalTgtMethod);
            }
            if (targetMethod != null) {
                doridlensMethod.callMethod(targetMethod);
            }
            DoridlensClass targetClass = classMap.get(target.getDeclaringClass());
            if (e.isVirtual() || e.isSpecial() || e.isStatic()) edgeOutCount++;
            //Detecting coupling (may include calls to inherited methods)
            if (targetClass != null && targetClass != currentClass) currentClass.coupledTo(targetClass);
        }
        while (edgeIntoIterator.hasNext()) {
            Edge e = edgeIntoIterator.next();
            if (e.isExplicit()) edgeIntoCount++;
        }
        MethodMetrics.createNumberOfDirectCalls(doridlensMethod, edgeOutCount);
        MethodMetrics.createNumberOfCallers(doridlensMethod, edgeIntoCount);
        AppMetrics.createNumberOfArgb8888(doridlensApp, argb8888Count);
    }

    public void collectClassMetrics(SootClass sootClass) {
        DoridlensModifiers modifier = DoridlensModifiers.PRIVATE;
        if (sootClass.isPublic()) {
            modifier = DoridlensModifiers.PUBLIC;
        } else if (sootClass.isProtected()) {
            modifier = DoridlensModifiers.PROTECTED;
        }

        DoridlensClass doridlensClass = DoridlensClass.createDoridlensClass(sootClass.getName(), this.doridlensApp, modifier);
        /*
        isStatic for classes doesn't work in this version of Soot.
        if(sootClass.isStatic()){
            IsStatic.createIsStatic(doridlensClass, true);
        }
        */
        if (sootClass.isFinal()) {
            CommonMetrics.createIsFinal(doridlensClass, true);
        }
        if (sootClass.isInnerClass()) {
            innerCount++;
            ClassMetrics.createIsInnerClass(doridlensClass, true);
            // Fix to determine if the class is static or not
            if (isInnerClassStatic(sootClass)) {
                CommonMetrics.createIsStatic(doridlensClass, true);
            }
        }
        if (isActivity(sootClass)) {
            activityCount++;
            ClassMetrics.createIsActivity(doridlensClass, true);
        } else if (isService(sootClass)) {
            serviceCount++;
            ClassMetrics.createIsService(doridlensClass, true);
        } else if (isView(sootClass)) {
            viewCount++;
            ClassMetrics.createIsView(doridlensClass, true);
        } else if (isAsyncTask(sootClass)) {
            asyncCount++;
            ClassMetrics.createIsAsyncTask(doridlensClass, true);
        } else if (isBroadcastReceiver(sootClass)) {
            broadcastReceiverCount++;
            ClassMetrics.createIsBroadcastReceiver(doridlensClass, true);
        } else if (isContentProvider(sootClass)) {
            contentProviderCount++;
            ClassMetrics.createIsContentProvider(doridlensClass, true);
        } else if (isApplication(sootClass)) {
            ClassMetrics.createIsApplication(doridlensClass, true);
        }
        if (sootClass.isAbstract()) {
            abstractCount++;
            CommonMetrics.createIsAbstract(doridlensClass, true);
        }
        if (sootClass.isInterface()) {
            interfaceCount++;
            ClassMetrics.createIsInterface(doridlensClass, true);
        }
        // Variable associated with classes
        for (SootField sootField : sootClass.getFields()) {
            modifier = DoridlensModifiers.PRIVATE;
            if (sootField.isPublic()) {
                modifier = DoridlensModifiers.PUBLIC;
            } else if (sootField.isProtected()) {
                modifier = DoridlensModifiers.PROTECTED;
            }
            DoridlensVariable doridlensVariable = DoridlensVariable.createDoridlensVariable(sootField.getName(), sootField.getType().toString(), modifier, doridlensClass);
            varCount++;
            if (sootField.isStatic()) {
                CommonMetrics.createIsStatic(doridlensVariable, true);
            }
            if (sootField.isFinal()) {
                CommonMetrics.createIsFinal(doridlensVariable, true);
            }
        }
        if (sootClass.hasSuperclass()) {
            doridlensClass.setParentName(sootClass.getSuperclass().getName());
        }
        this.classMap.put(sootClass, doridlensClass);
        // Number of methods including constructors
        CommonMetrics.createNumberOfMethods(doridlensClass, sootClass.getMethodCount());
        ClassMetrics.createDepthOfInheritance(doridlensClass, getDepthOfInheritance(sootClass));
        ClassMetrics.createNumberOfImplementedInterfaces(doridlensClass, sootClass.getInterfaceCount());
        ClassMetrics.createNumberOfAttributes(doridlensClass, sootClass.getFieldCount());
    }


    /**
     * Fix to determine if a class is static or not
     *
     * @param innerClass
     * @return
     */
    private boolean isInnerClassStatic(SootClass innerClass) {
        for (SootField sootField : innerClass.getFields()) {
            //we are looking if the field for non static inner class generated during the compilation (with the convention name) exists
            if (sootField.getName().equals("this$0")) {
                //in this case we can return false
                return false;
            }
        }
        return true;
    }

    public int getDepthOfInheritance(SootClass sootClass) {
        int doi = 0;
        do {
            doi++;
            sootClass = sootClass.getSuperclass();
        } while (sootClass.hasSuperclass());
        return doi;
    }

    public void computeInheritance() {
        for (Map.Entry entry : classMap.entrySet()) {
            SootClass sClass = (SootClass) entry.getKey();
            DoridlensClass pClass = (DoridlensClass) entry.getValue();
            SootClass sParent = sClass.getSuperclass();
            DoridlensClass pParent = classMap.get(sParent);
            if (pParent != null) {
                pClass.setParent(pParent);
            }
        }
    }

    public void computeInterface() {
        for (Map.Entry entry : classMap.entrySet()) {
            SootClass sClass = (SootClass) entry.getKey();
            DoridlensClass pClass = (DoridlensClass) entry.getValue();
            for (SootClass SInterface : sClass.getInterfaces()) {
                DoridlensClass pInterface = classMap.get(SInterface);
                if (pInterface != null) {
                    pClass.implement(pInterface);
                }
            }
        }
    }

    private boolean isActivity(SootClass sootClass) {
        return isSubClass(sootClass, "android.app.Activity");
    }

    private boolean isService(SootClass sootClass) {
        return isSubClass(sootClass, "android.app.Service");
    }

    private boolean isAsyncTask(SootClass sootClass) {
        return isSubClass(sootClass, "android.os.AsyncTask");
    }

    private boolean isView(SootClass sootClass) {
        return isSubClass(sootClass, "android.view.View");
    }

    private boolean isBroadcastReceiver(SootClass sootClass) {
        return isSubClass(sootClass, "android.content.BroadcastReceiver");
    }

    private boolean isContentProvider(SootClass sootClass) {
        return isSubClass(sootClass, "android.content.ContentProvider");
    }

    private boolean isApplication(SootClass sootClass) {
        return isSubClass(sootClass, "android.app.Application");
    }

    private boolean isSubClass(SootClass sootClass, String className) {
        do {
            if (sootClass.getName().equals(className)) return true;
            sootClass = sootClass.getSuperclass();
        } while (sootClass.hasSuperclass());
        return false;
    }

    private boolean isOverride(SootMethod sootMethod) {
        SootClass sootClass = sootMethod.getDeclaringClass();
        for (SootClass inter : sootClass.getInterfaces()) {
            if (classContainsMethod(inter, sootMethod)) return true;
            while (inter.hasSuperclass()) {
                inter = inter.getSuperclass();
                if (classContainsMethod(inter, sootMethod)) return true;
            }
        }
        while (sootClass.hasSuperclass()) {
            sootClass = sootClass.getSuperclass();
            if (classContainsMethod(sootClass, sootMethod)) return true;
        }
        return false;
    }

    /**
     * Test if a class contains a method with same name, parameters and return type
     *
     * @param sootClass
     * @param sootMethod
     * @return
     */
    private boolean classContainsMethod(SootClass sootClass, SootMethod sootMethod) {
        //Here unsafe just means it will return null (instead of throwing an exception).
        if (sootClass.getMethodUnsafe(sootMethod.getName(), sootMethod.getParameterTypes(), sootMethod.getReturnType()) != null)
            return true;
        else return false;
    }
}

