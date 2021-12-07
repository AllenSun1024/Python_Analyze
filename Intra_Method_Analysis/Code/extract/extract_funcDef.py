import ast
import astunparse
from pprint import pprint

class FuncDefExtractor(ast.NodeVisitor):
    def __init__(self):
        self.funcStats = {
            "name": [],
            "args": [],
            "callNodes": [],
            "APIs": []
        }
        self.callNodes = []
        self.APIs = []
        self.isInFunc = False

    def visit_FunctionDef(self, node):
        self.isInFunc = True
        self.generic_visit(node)
        self.funcStats["callNodes"].append(self.callNodes)
        self.callNodes = []
        self.funcStats["APIs"].append(self.APIs)
        self.APIs = []
        self.funcStats["name"].append(node.name)
        args = []
        if node.args.posonlyargs is not None:
            for arg in node.args.posonlyargs:
                args.append(arg.arg)
        if node.args.args is not None:
            for arg in node.args.args:
                args.append(arg.arg)
        if node.args.kwonlyargs:
            for arg in node.args.kwonlyargs:
                args.append(arg.arg)
        if node.args.vararg is not None:
            args.append(node.args.vararg.arg)
        if node.args.kwarg is not None:
            args.append(node.args.kwarg.arg)
        self.funcStats["args"].append(args)
        self.isInFunc = False

    def visit_Call(self, node):
        if self.isInFunc:
            self.callNodes.append(astunparse.unparse(node))
            self.generic_visit(node)
            name = self.get_Call_Name(node, '')
            if name != '' and name is not None:
                self.APIs.append(name)

    def get_Call_Name(self, node, name):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                return node.func.id + '.' + name
            elif isinstance(node.func, ast.Attribute):
                name = node.func.attr + '.' + name
                if isinstance(node.func.value, ast.Name):
                    return node.func.value.id + '.' + name
                else:
                    return self.get_Call_Name(node.func.value, name)
        elif isinstance(node, ast.Attribute):
            name = node.attr + '.' + name
            if isinstance(node.value, ast.Name):
                return node.value.id + '.' + name
            else:
                return self.get_Call_Name(node.value, name)
        elif isinstance(node, ast.Subscript):
            if isinstance(node.value, ast.Name):
                return node.value.id + '.' + name
            else:
                return self.get_Call_Name(node.value, name)
        else:
            return None

    def report(self):
        with open('result.txt', 'a') as f:
            for i in range(len(self.funcStats["name"])):
                f.write(self.funcStats["name"][i])
                f.write(':\n')
                for item in self.funcStats["APIs"][i]:
                    f.write(item)
                    f.write('\n')
                f.write('\n')
                pprint(self.funcStats["name"][i])
                pprint(self.funcStats["APIs"][i])
                print('\n')
            f.write('--------------------------------------------\n\n')
            print('\n\n')
