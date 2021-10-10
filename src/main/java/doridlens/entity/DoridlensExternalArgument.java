package doridlens.entity;

/**
 * Author: MaoMorn
 * Date: 2020/1/2
 * Time: 9:20
 * Description:
 */
public class DoridlensExternalArgument extends Entity{
    private DoridlensExternalMethod doridlensExternalMethod;
    private int position;

    private DoridlensExternalArgument(String name, int position, DoridlensExternalMethod doridlensExternalMethod) {
        this.doridlensExternalMethod = doridlensExternalMethod;
        this.name = name;
        this.position = position;
    }

    public static DoridlensExternalArgument createDoridlensExternalArgument(String name, int position, DoridlensExternalMethod doridlensExternalMethod){
        DoridlensExternalArgument doridlensExternalArgument = new DoridlensExternalArgument(name,position,doridlensExternalMethod);
        doridlensExternalMethod.addExternalArgument(doridlensExternalArgument);
        return doridlensExternalArgument;
    }

    public int getPosition() {
        return position;
    }
}
