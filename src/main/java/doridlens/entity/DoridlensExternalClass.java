package doridlens.entity;

import java.util.HashSet;
import java.util.Set;

/**
 * Author: MaoMorn
 * Date: 2020/1/2
 * Time: 9:21
 * Description:
 */
public class DoridlensExternalClass extends Entity{
    private DoridlensApp doridlensApp;
    private String parentName;
    private Set<DoridlensExternalMethod> doridlensExternalMethods;

    public Set<DoridlensExternalMethod> getDoridlensExternalMethods() {
        return doridlensExternalMethods;
    }

    public String getParentName() {
        return parentName;
    }

    public void setParentName(String parentName) {
        this.parentName = parentName;
    }

    private DoridlensExternalClass(String name, DoridlensApp doridlensApp) {
        this.setName(name);
        this.doridlensApp = doridlensApp;
        this.doridlensExternalMethods  = new HashSet<>();
    }

    public static DoridlensExternalClass createDoridlensExternalClass(String name, DoridlensApp doridlensApp) {
        DoridlensExternalClass doridlensClass = new DoridlensExternalClass(name, doridlensApp);
        doridlensApp.addDoridlensExternalClass(doridlensClass);
        return doridlensClass;
    }

    public void addDoridlensExternalMethod(DoridlensExternalMethod doridlensMethod){
        doridlensExternalMethods.add(doridlensMethod);
    }

    public DoridlensApp getDoridlensApp() {
        return doridlensApp;
    }

    public void setDoridlensApp(DoridlensApp doridlensApp) {
        this.doridlensApp = doridlensApp;
    }

}

