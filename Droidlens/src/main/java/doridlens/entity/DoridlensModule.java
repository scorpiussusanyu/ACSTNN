package doridlens.entity;

/**
 * Author: MaoMorn
 * Date: 2020/1/2
 * Time: 22:02
 * Description:
 */
public class DoridlensModule extends Entity {
    private String name;
    private String rootPath;
    private String androidManifest;

    private DoridlensModule(String name, String rootPath, String androidManifest) {
        this.name = name;
        this.rootPath = rootPath;
        this.androidManifest = androidManifest;
    }

    public static DoridlensModule createDoridlensModule(String name, String rootPath, String androidManifest, DoridlensApp doridlensApp) {
        DoridlensModule doridlensModule = new DoridlensModule(name, rootPath, androidManifest);
        doridlensApp.addDoridlensModule(doridlensModule);
        return doridlensModule;
    }

    @Override
    public String getName() {
        return name;
    }

    public String getRootPath() {
        return rootPath;
    }

    public String getAndroidManifest() {
        return androidManifest;
    }
}
