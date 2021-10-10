package doridlens.entity;

/**
 * Author: MaoMorn
 * Date: 2020/1/2
 * Time: 9:22
 * Description:
 */
public class DoridlensVariable extends Entity{
    private DoridlensClass doridlensClass;
    private String type;
    private DoridlensModifiers modifier;

    public String getType() {
        return type;
    }

    public DoridlensModifiers getModifier() {
        return modifier;
    }

    private DoridlensVariable(String name, String type, DoridlensModifiers modifier, DoridlensClass doridlensClass) {
        this.type = type;
        this.name = name;
        this.modifier = modifier;
        this.doridlensClass = doridlensClass;
    }

    public static DoridlensVariable createDoridlensVariable(String name, String type, DoridlensModifiers modifier, DoridlensClass doridlensClass) {
        DoridlensVariable doridlensVariable = new DoridlensVariable(name, type, modifier, doridlensClass);
        doridlensClass.addDoridlensVariable(doridlensVariable);
        return doridlensVariable;
    }

    public boolean isPublic(){
        return modifier == DoridlensModifiers.PUBLIC;
    }

    public boolean isPrivate(){
        return modifier == DoridlensModifiers.PRIVATE;
    }

    public boolean isProtected(){ return modifier == DoridlensModifiers.PROTECTED; }
}

