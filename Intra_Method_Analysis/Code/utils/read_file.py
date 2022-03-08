import os
import ast
import jedi


class GetProject:
    def __init__(self, path, project):
        try:
            with open(path) as f:
                data = f.read()
            self.tree = ast.parse(data, path)
            self.script = jedi.Script(data, path=path, project=project)
        except Exception as e:
            """
            将Python2转换成Python3，以兼容不同版本的Python
            """
            print(e)
            print("[Futurizing] %s" % path)
            try:
                os.system("futurize --stage1 -w %s" % path)
                with open(path) as f:
                    data = f.read()
                self.tree = ast.parse(data, path)
                self.script = jedi.Script(data, path=path, project=project)
            except Exception as e:
                print(e)
                print("Failed to futurize")
                self.tree = None
                self.script = None


def scan_one_file(path, project):
    """
    解析单个Python文件
    :param path: 单个Python文件路径
    :param project: 单个文件所在项目路径
    :return tree: Python AST
    :return script: jedi.Script
    """
    print("[Scanning] %s" % str(path))
    resultPath = '/' + '/'.join(((str(path)).split('/'))[1:-3]) + '/TestResult/' + ((str(path)).split('/'))[-2] + '/' + ((((str(path)).split('/'))[-1]).split('.'))[0] + '.txt'
    file_data = GetProject(path, project)
    tree = file_data.tree
    script = file_data.script
    return tree, script, resultPath
