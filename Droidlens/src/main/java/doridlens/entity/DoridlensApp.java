package doridlens.entity;

import java.util.ArrayList;
import java.util.List;

/**
 * Author: MaoMorn
 * Date: 2020/1/2
 * Time: 9:19
 * Description:
 */
public class DoridlensApp extends Entity {
    private String pack; //Package
    private List<DoridlensClass> doridlensClasses;
    private List<DoridlensModule> doridlensModules;
    private List<DoridlensExternalClass> doridlensExternalClasses;

    private DoridlensApp(String name, String pack) {
        this.name = name;
        this.pack = pack;
        this.doridlensModules = new ArrayList<>();
        this.doridlensClasses = new ArrayList<>();
        this.doridlensExternalClasses = new ArrayList<>();
    }

    public List<DoridlensExternalClass> getDoridlensExternalClasses() {
        return doridlensExternalClasses;
    }

    public void addDoridlensExternalClass(DoridlensExternalClass doridlensExternalClass) {
        doridlensExternalClasses.add(doridlensExternalClass);
    }

    public List<DoridlensClass> getDoridlensClasses() {
        return doridlensClasses;
    }

    public void addDoridlensClass(DoridlensClass doridlensClass) {
        doridlensClasses.add(doridlensClass);
    }

    public void addDoridlensModule(DoridlensModule doridlensModule) {
        doridlensModules.add(doridlensModule);
    }

    public List<DoridlensModule> getDoridlensModule() {
        return doridlensModules;
    }

    public static DoridlensApp createDoridlensApp(String name, String pack) {
        return new DoridlensApp(name, pack);
    }

    public String getPack() {
        return pack;
    }
}
