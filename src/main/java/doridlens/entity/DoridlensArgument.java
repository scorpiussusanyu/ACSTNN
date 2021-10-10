package doridlens.entity;

/**
 * Author: MaoMorn
 * Date: 2020/1/2
 * Time: 9:20
 * Description:
 */
public class DoridlensArgument extends Entity{
    private DoridlensMethod doridlensMethod;
    private int position;

    private DoridlensArgument(String name, int position, DoridlensMethod doridlensMethod) {
        this.doridlensMethod = doridlensMethod;
        this.name = name;
        this.position = position;
    }

    public static DoridlensArgument createDoridlensArgument(String name, int position, DoridlensMethod doridlensMethod){
        DoridlensArgument doridlensArgument = new DoridlensArgument(name,position,doridlensMethod);
        doridlensMethod.addArgument(doridlensArgument);
        return doridlensArgument;
    }

    public int getPosition() {
        return position;
    }
}
