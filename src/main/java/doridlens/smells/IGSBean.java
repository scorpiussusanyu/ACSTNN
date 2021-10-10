package doridlens.smells;

import com.github.javaparser.ast.Modifier;
import com.github.javaparser.ast.NodeList;
import com.github.javaparser.ast.body.FieldDeclaration;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.expr.FieldAccessExpr;
import com.github.javaparser.ast.expr.MethodCallExpr;

import java.util.ArrayList;

/**
 * Author: MaoMorn
 * Date: 2020/1/6
 * Time: 8:43
 * Description:
 */
public class IGSBean {
    private int TAG = 0;
    private FieldDeclaration field;
    private MethodDeclaration smell;
    private ArrayList<MethodCallExpr> calledList;

    public IGSBean(int tag, FieldDeclaration field, MethodDeclaration smell) {
        this.TAG = tag;
        this.field = field;
        this.smell = smell;
        this.calledList = new ArrayList<>();
    }

    public void addCalled(MethodCallExpr expression) {
        this.calledList.add(expression);
    }

    public void refactor() {
        NodeList<Modifier> modifiers = field.getModifiers();
        if (modifiers == null) {
            modifiers = new NodeList<>();
            field.setModifiers(new NodeList<Modifier>());
        }
        if (modifiers.size() == 0) {
            modifiers.add(Modifier.publicModifier());
        } else {
            String modifier = modifiers.get(0).
                    getKeyword().asString();
            if (modifier.equals("protected") || modifier.equals("private")) {
                modifiers.set(0, Modifier.publicModifier());
            } else {
                modifiers.add(0, Modifier.publicModifier());
            }
        }
        smell.getParentNode().get().remove(smell);
        FieldAccessExpr fieldAccessExpr;
        for (MethodCallExpr callExpr : calledList) {
            fieldAccessExpr = new FieldAccessExpr(
                    callExpr.getScope().get(),
                    field.getVariable(0).toString());
            callExpr.getParentNode().get().
                    replace(callExpr, fieldAccessExpr);
        }
    }
}
