package doridlens.entity;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

/**
 * Author: MaoMorn
 * Date: 2020/1/2
 * Time: 9:21
 * Description:
 */
public class DoridlensMethod extends Entity{
    private DoridlensClass doridlensClass;
    private String returnType;
    private Set<DoridlensVariable> usedVariables;
    private Set<Entity> calledMethods;
    private DoridlensModifiers modifier;
    private List<DoridlensArgument> arguments;
    public String getReturnType() {
        return returnType;
    }

    public DoridlensModifiers getModifier() {
        return modifier;
    }

    private DoridlensMethod(String name, DoridlensModifiers modifier, String returnType, DoridlensClass doridlensClass) {
        this.setName(name);
        this.doridlensClass = doridlensClass;
        this.usedVariables = new HashSet<>(0);
        this.calledMethods = new HashSet<>(0);
        this.arguments = new ArrayList<>(0);
        this.modifier = modifier;
        this.returnType = returnType;
    }

    public static DoridlensMethod createDoridlensMethod(String name, DoridlensModifiers modifier, String returnType, DoridlensClass doridlensClass) {
        DoridlensMethod doridlensMethod = new DoridlensMethod(name, modifier, returnType, doridlensClass);
        doridlensClass.addDoridlensMethod(doridlensMethod);
        return  doridlensMethod;
    }

    public DoridlensClass getDoridlensClass() {
        return doridlensClass;
    }

    public void setDoridlensClass(DoridlensClass doridlensClass) {
        this.doridlensClass = doridlensClass;
    }

    @Override
    public String toString() {
        return this.getName() + "#" + doridlensClass;
    }

    public void useVariable(DoridlensVariable doridlensVariable) {
        usedVariables.add(doridlensVariable);
    }

    public Set<DoridlensVariable> getUsedVariables(){
        return this.usedVariables;
    }

    public void callMethod(Entity doridlensMethod) { calledMethods.add(doridlensMethod);}

    public Set<Entity> getCalledMethods() { return this.calledMethods; }

    public boolean haveCommonFields(DoridlensMethod doridlensMethod){
        Set<DoridlensVariable> otherVariables = doridlensMethod.getUsedVariables();
        for(DoridlensVariable doridlensVariable : usedVariables){
            if(otherVariables.contains(doridlensVariable)) return true;
        }
        return false;
    }

    public void addArgument(DoridlensArgument doridlensArgument){
        this.arguments.add(doridlensArgument);
    }

    public List<DoridlensArgument> getArguments(){
        return arguments;
    }
}

