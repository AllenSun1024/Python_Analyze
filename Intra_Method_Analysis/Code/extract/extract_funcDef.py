import ast
from pprint import pprint

class FuncDefExtractor(ast.NodeVisitor):
    def __init__(self, script):
        self.funcStats = {
            "name": [],  # 当前文件内定义的函数名列表, [name1, name2, ...]
            "args": [],  # 函数参数, [[1's arg], [2's arg], ...]
            "APIs": [],  # 函数中调用的API列表, [[f1_api_1, f1_api_2, ...], ...]
            "lineNo": [],  # 每个被调用API的起始行号, [[f1_line_1, f1_line_2, ...], ...]
            "end_lineNo": [],  # 每个被调用API的结束行号，用于应对API跨行的Case
            "variables": []
        }
        self.APIs = []
        self.lines = []
        self.end_lines = []
        self.variables = []  # 记录每个函数中被定义的变量
        self.isInFunc = False
        self.script = script

    def visit_FunctionDef(self, node):
        """
        解析函数定义
        我们做的是函数内解析，所以这算是解析入口
        """
        self.isInFunc = True
        self.generic_visit(node)
        self.funcStats["APIs"].append(self.APIs)
        self.APIs = []
        self.funcStats["lineNo"].append(self.lines)
        self.lines = []
        self.funcStats["end_lineNo"].append(self.end_lines)
        self.end_lines = []
        self.funcStats["variables"].append(self.variables)
        self.variables = []
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
            self.generic_visit(node)
            name = self.get_Call_Name(node, '')
            if name != '' and name is not None:
                self.APIs.append(name[:-1])
                self.lines.append(node.lineno)
                self.end_lines.append(node.end_lineno)

    def visit_Lambda(self, node):
        pass

    def visit_Assign(self, node):
        if self.isInFunc:
            self.generic_visit(node)
            # if isinstance(node, ast.Name):
            #     print(node.id)
            print(node)
            # name = self.get_Var_name(node, '')
            # print(name)
            # if name != '' and name is not None:
            #     variables = []
            #     for target in node.targets:
            #         variable = []
            #         name = self.get_Call_Name(target, '')
            #         variable.append(name)  # name除了为正常变量名字符串外，可能为空串，也可能为None
            #         variable.append(target.lineno)
            #         variable.append(target.end_lineno)
            #         variable.append(target.col_offset)
            #         variable.append(target.end_col_offset)
            #         variables.append(variable)
            #     self.variables.append(variables)

    def get_Call_Name(self, node, name):
        """
        递归解析, 得到被调用函数完整的名字
        """
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):  # 递归出口1
                return node.func.id + '.' + name
            elif isinstance(node.func, ast.Attribute):
                name = node.func.attr + '.' + name
                if isinstance(node.func.value, ast.Name):  # 递归出口2
                    return node.func.value.id + '.' + name
                else:
                    return self.get_Call_Name(node.func.value, name)
        elif isinstance(node, ast.Attribute):
            name = node.attr + '.' + name
            if isinstance(node.value, ast.Name):  # 递归出口3
                return node.value.id + '.' + name
            else:
                return self.get_Call_Name(node.value, name)
        elif isinstance(node, ast.Subscript):
            if isinstance(node.value, ast.Name):  # 递归出口4
                return node.value.id + '.' + name
            else:
                return self.get_Call_Name(node.value, name)
        else:
            return None

    # def get_Var_name(self, node, name):
    #     if isinstance(node, ast.Name):
    #         return node.id + name
    #     # elif isinstance(node, ast.Attribute):
    #     #     name = node.attr + '.' + name
    #     #     if isinstance(node.value, ast.Name):
    #     #         return node.value.id + '.' + name
    #     #     else:
    #     #         return self.get_Var_name(node.value, name)
    #     else:
    #         return None

    def report(self):
        with open('result.txt', 'a') as f:
            for i in range(len(self.funcStats["name"])):  # 一个源文件中可能定义多个函数
                # for j in range(len(self.funcStats["variables"][i])):
                #     pprint(self.funcStats["variables"][i][j])
                f.write(self.funcStats["name"][i])  # 第i个函数的名字
                f.write(':\n')
                for subs in range(len(self.funcStats["APIs"][i])):  # 第i个函数中有若干API调用
                    if self.funcStats["APIs"][i][subs] is not None:
                        f.write(self.funcStats["APIs"][i][subs])
                        f.write(' ')
                        f.write(str(self.funcStats["lineNo"][i][subs]))
                        f.write(' ')
                        f.write(str(self.funcStats["end_lineNo"][i][subs]))
                        f.write('\n')
                f.write('\n')
            f.write('--------------------------------------------\n\n')
