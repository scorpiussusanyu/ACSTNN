package doridlens.entity;

import java.util.ArrayList;
import java.util.List;

/**
 * Author: MaoMorn
 * Date: 2020/1/2
 * Time: 9:21
 * Description:
 */
public class DoridlensExternalMethod extends Entity {
    private DoridlensExternalClass doridlensExternalClass;
    private List<DoridlensExternalArgument> doridlensExternalArguments;
    private String returnType;

    public String getReturnType() {
        return returnType;
    }

    public List<DoridlensExternalArgument> getDoridlensExternalArguments() {
        return doridlensExternalArguments;
    }

    private DoridlensExternalMethod(String name, String returnType, DoridlensExternalClass doridlensExternalClass) {
        this.setName(name);
        this.doridlensExternalClass = doridlensExternalClass;
        this.returnType = returnType;
        this.doridlensExternalArguments = new ArrayList<>();
    }

    public static DoridlensExternalMethod createDoridlensExternalMethod(String name, String returnType, DoridlensExternalClass doridlensClass) {
        DoridlensExternalMethod doridlensMethod = new DoridlensExternalMethod(name, returnType, doridlensClass);
        doridlensClass.addDoridlensExternalMethod(doridlensMethod);
        return  doridlensMethod;
    }

    public DoridlensExternalClass getDoridlensExternalClass() {
        return doridlensExternalClass;
    }

    public void setDoridlensExternalClass(DoridlensExternalClass doridlensClass) {
        this.doridlensExternalClass = doridlensClass;
    }

    @Override
    public String toString() {
        return this.getName() + "#" + doridlensExternalClass;
    }

    public void addExternalArgument(DoridlensExternalArgument doridlensExternalArgument) {
        this.doridlensExternalArguments.add(doridlensExternalArgument);
    }
}

