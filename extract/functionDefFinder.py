import ast
import astunparse

class FunctionDefFinder(ast.NodeVisitor):
    def __init__(self):
        self.callNodes = []
        self.eachFunc = []
        self.flag = False

    def visit_FunctionDef(self, node):
        self.flag = True
        self.generic_visit(node)
        self.eachFunc.append(self.callNodes)
        self.callNodes = []
        self.flag = False

    def visit_Call(self, node):
        if self.flag:  # CallNode is in FunctionDef
            self.callNodes.append(astunparse.unparse(node))

    def report(self):
        print(self.eachFunc)
