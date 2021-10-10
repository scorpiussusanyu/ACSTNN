package doridlens.entity;

import java.util.HashSet;
import java.util.Set;

/**
 * Author: MaoMorn
 * Date: 2020/1/2
 * Time: 9:20
 * Description:
 */
public class DoridlensClass extends Entity{
    private DoridlensApp doridlensApp;
    private DoridlensClass parent;
    //parent name to cover library case
    private String parentName;
    private int complexity;
    private int children;
    private Set<DoridlensClass> coupled;
    private Set<DoridlensMethod> doridlensMethods;
    private Set<DoridlensVariable> doridlensVariables;
    private Set<DoridlensClass> interfaces;
    private DoridlensModifiers modifier;

    public DoridlensModifiers getModifier() {
        return modifier;
    }

    public Set<DoridlensVariable> getDoridlensVariables() {
        return doridlensVariables;
    }

    public Set<DoridlensMethod> getDoridlensMethods() {
        return doridlensMethods;
    }

    public String getParentName() {
        return parentName;
    }

    public void setParentName(String parentName) {
        this.parentName = parentName;
    }

    private DoridlensClass(String name, DoridlensApp doridlensApp, DoridlensModifiers modifier) {
        this.setName(name);
        this.doridlensApp = doridlensApp;
        this.complexity = 0;
        this.children = 0;
        this.doridlensMethods  = new HashSet<>();
        this.doridlensVariables = new HashSet<>();
        this.coupled = new HashSet<>();
        this.interfaces = new HashSet<>();
        this.modifier = modifier;
    }

    public static DoridlensClass createDoridlensClass(String name, DoridlensApp doridlensApp, DoridlensModifiers modifier) {
        DoridlensClass doridlensClass = new DoridlensClass(name, doridlensApp, modifier);
        doridlensApp.addDoridlensClass(doridlensClass);
        return doridlensClass;
    }

    public DoridlensClass getParent() {
        return parent;
    }

    public Set<DoridlensClass> getInterfaces(){ return interfaces;}

    public void setParent(DoridlensClass parent) {
        this.parent = parent;
    }

    public void addDoridlensMethod(DoridlensMethod doridlensMethod){
        doridlensMethods.add(doridlensMethod);
    }

    public DoridlensApp getDoridlensApp() {
        return doridlensApp;
    }

    public void setDoridlensApp(DoridlensApp doridlensApp) {
        this.doridlensApp = doridlensApp;
    }

    public void addComplexity(int value){
        complexity += value;
    }

    public void addChildren() { children += 1;}

    public int getComplexity() {
        return complexity;
    }

    public int getChildren() { return children; }

    public void coupledTo(DoridlensClass doridlensClass){ coupled.add(doridlensClass);}

    public void implement(DoridlensClass doridlensClass){ interfaces.add(doridlensClass);}

    public int getCouplingValue(){ return coupled.size();}

    public int computeLCOM(){
        Object methods[] = doridlensMethods.toArray();
        int methodCount = methods.length;
        int haveFieldInCommon = 0;
        int noFieldInCommon  = 0;
        for(int i=0; i< methodCount;i++){
            for(int j=i+1; j < methodCount; j++){
                if( ((DoridlensMethod) methods[i]).haveCommonFields((DoridlensMethod) methods[j])){
                    haveFieldInCommon++;
                }else{
                    noFieldInCommon++;
                }
            }
        }
        int LCOM =  noFieldInCommon - haveFieldInCommon;
        return LCOM > 0 ? LCOM : 0;
    }

    /**
     Get the NPath complexity of the entire program
     The NPath complexity is just the combinatorial of the cyclomatic complexity
     **/
    public double computeNPathComplexity() {
        return Math.pow(2.0, (double) getComplexity());
    }

    public void addDoridlensVariable(DoridlensVariable doridlensVariable) {
        doridlensVariables.add(doridlensVariable);
    }

    public DoridlensVariable findVariable(String name){
        // First we are looking to the field declared by this class (any modifiers)
        for (DoridlensVariable doridlensVariable : doridlensVariables){
            if (doridlensVariable.getName().equals(name)) return doridlensVariable;
        }
        //otherwise we return null
        return null;
    }
}

