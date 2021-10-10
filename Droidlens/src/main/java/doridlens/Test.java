package doridlens;

import com.github.javaparser.JavaParser;
import com.github.javaparser.ParserConfiguration;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.expr.FieldAccessExpr;
import com.github.javaparser.ast.visitor.ModifierVisitor;
import com.github.javaparser.ast.visitor.Visitable;
import com.github.javaparser.resolution.types.ResolvedType;
import com.github.javaparser.symbolsolver.JavaSymbolSolver;
import com.github.javaparser.symbolsolver.resolution.typesolvers.CombinedTypeSolver;
import com.github.javaparser.symbolsolver.resolution.typesolvers.ReflectionTypeSolver;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;

/**
 * Author: MaoMorn
 * Date: 2020/1/2
 * Time: 9:49
 * Description:
 */
public class Test {
    public static void main(String[] args) throws IOException {
//        String dbPath = "D:\\DataBase\\Neo4j CE 3.3.1\\data\\K-9 Mail_5.600.db";
//        QueryEngine engine = new QueryEngine(dbPath);
//        GraphDatabaseService sevice = engine.getGraphDatabaseService();
//        try (Transaction ignored = sevice.beginTx()) {
//            String query = "MATCH (c:Class) RETURN c.name as name,EXISTS(c.is_inner_class) as is_inner_class," +
//                    "EXISTS(c.is_static) as is_static,EXISTS(c.is_interface) as is_interface,EXISTS(c.is_activity) as is_activity";
//            String query1 = "MATCH (c:Class) WHERE EXISTS(c.is_inner_class) AND NOT EXISTS(c.is_static) RETURN c.name as name,EXISTS(c.is_inner_class) as is_inner_class," +
//                    "EXISTS(c.is_static) as is_static,EXISTS(c.is_interface) as is_interface,EXISTS(c.is_activity) as is_activity";
//            String query2 = "MATCH (c:Class) RETURN c.number_of_methods,c.depth_of_inheritance,c.number_of_implemented_interfaces,c.number_of_attributes," +
//                    "c.number_of_children,c.class_complexity,c.coupling_between_objects,c.lack_of_cohesion_in_methods, CASE EXISTS(c.is_inner_class) WHEN TRUE THEN 1 ELSE 0 END as is_inner_class,CASE EXISTS(c.is_static) WHEN TRUE THEN 1 ELSE 0 END as is_static,CASE EXISTS(c.is_inner_class) AND NOT EXISTS(c.is_static) WHEN TRUE THEN 1 ELSE 0 END as result";
//            Result result = sevice.execute(query2);
//            engine.resultToCSV(result, "data.csv");
//        } catch (IOException e) {
//            e.printStackTrace();
//        }
//        String sourcePath = "E:\\AndroidStudioProjects\\Sample";
//        SourceAnalyzer analyzer = new SourceAnalyzer(sourcePath, "JumpGo", "aaa", false);
//        analyzer.init();
//        analyzer.runAnalysis();
//
//        System.out.println(Modifier.publicModifier().getKeyword().asString());
        String path = "C:\\Users\\MaoMorn\\Desktop\\android\\apks";
        File file = new File(path);
        File[] list = file.listFiles();
        ArrayList<String> backup = new ArrayList<>();
        for (File f : list) {
            for (File fl : f.listFiles()) {
                String source = fl.getAbsolutePath();
                String target = source.replaceFirst("apks", "paprika") + fl.getName().substring(0, fl.getName().length() - 4)+".db";
//                String analysis=""
                System.out.println(source);
                System.out.println(target);
                try {
                } catch (Exception e) {
                    backup.add(source);
                }
            }
        }
        System.out.println("failed applications");
        for (String s : backup) {
            System.out.println(s);
        }
//        analyse "G:\测试应用\K-9 Mail\v5.600\k9-5.600.apk" - a "D:\Android\sdk\platforms" - db
//        "D:\DataBase\Neo4j CE 3.3.1\data\K-9 Mail_5.600.db" - n "K-9 Mail" - p "com.fsck.k9" - u "unsafe" - omp True
    }

    public static void main1(String[] args) {
        CombinedTypeSolver combinedTypeSolver = new CombinedTypeSolver();
        combinedTypeSolver.add(new ReflectionTypeSolver());
        JavaSymbolSolver symbolSolver = new JavaSymbolSolver(combinedTypeSolver);
        ParserConfiguration parserConfiguration = new ParserConfiguration().setSymbolResolver(symbolSolver);
        JavaParser parser = new JavaParser(parserConfiguration);
        CompilationUnit compilationUnit = parser.parse(
                "import java.io.File;\n" +
                        "\n" +
                        "public class Main {\n" +
                        "    static String s = File.separator;\n" +
                        "    public static void main(String args[]) {\n" +
                        "        System.out.println(s);\n" +
                        "    }\n" +
                        "}\n").getResult().get();
        compilationUnit.accept(
                new ModifierVisitor<Void>() {
                    @Override
                    public Visitable visit(final FieldAccessExpr n, final Void arg) {
                        System.out.println(n);
                        try { // this does not work!!!
                            ResolvedType resolvedType = n.getScope().calculateResolvedType();
                            System.out.println(resolvedType.describe());
                        } catch (Exception e) {
                            e.printStackTrace();
                        }

                        return super.visit(n, arg);
                    }
                },
                null
        );
    }
}
