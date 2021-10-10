package doridlens.analyzer;

import com.github.javaparser.ParseResult;
import com.github.javaparser.ParserConfiguration;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.symbolsolver.JavaSymbolSolver;
import com.github.javaparser.symbolsolver.javaparsermodel.JavaParserFacade;
import com.github.javaparser.symbolsolver.resolution.typesolvers.CombinedTypeSolver;
import com.github.javaparser.symbolsolver.resolution.typesolvers.JarTypeSolver;
import com.github.javaparser.symbolsolver.resolution.typesolvers.JavaParserTypeSolver;
import com.github.javaparser.symbolsolver.resolution.typesolvers.ReflectionTypeSolver;
import com.github.javaparser.utils.SourceRoot;
import doridlens.entity.DoridlensApp;
import doridlens.entity.DoridlensModule;
import doridlens.utility.Utilities;

import java.io.File;
import java.util.List;
import java.util.logging.Logger;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

/**
 * Author: MaoMorn
 * Date: 2020/1/2
 * Time: 16:25
 * Description:
 */
public class SourceAnalyzer extends Analyzer {
    private final static Logger LOGGER = Logger.getLogger(SourceAnalyzer.class.getName());
    private boolean mainPackageOnly = false;
    private String sourcePath;
    private String name;
    private String pack;
    private DoridlensApp doridlensApp;

    public SourceAnalyzer(String sourcePath, String name, String pack, boolean mainPackageOnly) {
        this.sourcePath = sourcePath;
        this.name = name;
        this.pack = pack;
        this.mainPackageOnly = mainPackageOnly;
        this.doridlensApp = DoridlensApp.createDoridlensApp(name, pack);
    }


    @Override
    public void init() {
        initModules();
    }

    @Override
    public void runAnalysis() {
        SourceRoot sourceRoot = new SourceRoot(new File(sourcePath).toPath());
        try {
            CombinedTypeSolver typeSolver = new CombinedTypeSolver();
            for (DoridlensModule module : doridlensApp.getDoridlensModule()) {
                typeSolver.add(new JavaParserTypeSolver(new File(module.getRootPath())));
            }
            typeSolver.add(new JarTypeSolver("D:\\Android\\sdk\\platforms\\android-28\\android.jar"));
            typeSolver.add(new ReflectionTypeSolver());
            ParserConfiguration parserConfiguration = new ParserConfiguration().setSymbolResolver(new JavaSymbolSolver(typeSolver));
            sourceRoot.setParserConfiguration(parserConfiguration);
            List<ParseResult<CompilationUnit>> parseResults = sourceRoot.tryToParse("");
            List<CompilationUnit> allCus = parseResults.stream().map(r -> r.getResult().get()).collect(Collectors.toList());
            System.out.println("");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    @Override
    public DoridlensApp getDoridlensApp() {
        return doridlensApp;
    }

    private void initModules() {
        File settingsFile = new File(sourcePath + "\\settings.gradle");
        if (settingsFile.exists()) {
            String source = Utilities.readFile(settingsFile.getPath());
            String regex = "(//[\\s\\S]*\\n)|(/\\*([\\s\\S]*)\\*/)";
            Matcher matcher = Pattern.compile(regex, Pattern.MULTILINE).matcher(source);
            String result = matcher.replaceAll("");
            regex = "'([^']*)'";
            matcher = Pattern.compile(regex).matcher(result);
            while (matcher.find()) {
                String temp = matcher.group();
                File module;
                String path = "";
                if (temp.length() > 3) {
                    temp = temp.substring(1, temp.length() - 1);
                    path = temp.replace(":", "\\");
                    module = new File(sourcePath + path + "\\src");
                } else {
                    temp = ":";
                    module = new File(sourcePath + "\\src");
                }
                if (module.exists()) {
                    DoridlensModule.createDoridlensModule(temp, module.getPath(), source + path + "\\AndroidManifest.xml", doridlensApp);
                } else {
                    module = new File(source + path + "\\src\\main\\java");
                    if (module.exists()) {
                        DoridlensModule.createDoridlensModule(temp, module.getPath(), source + path + "\\src\\main\\AndroidManifest.xml", doridlensApp);
                    }
                }
            }
        }
    }
}
