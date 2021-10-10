package doridlens.analyzer;

import doridlens.entity.DoridlensApp;

/**
 * Author: MaoMorn
 * Date: 2020/1/2
 * Time: 9:16
 * Description:
 */
public abstract class Analyzer {
    public abstract void init();
    public abstract void runAnalysis();
    public abstract DoridlensApp getDoridlensApp();
}
