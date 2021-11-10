import os
import ast
import jedi

class GetDataFromFile:
    def __init__(self, path, project):
        try:
            with open(path) as f:
                data = f.read()
            self.tree = ast.parse(data, path)
            self.script = jedi.Script(data, path=path, project=project)
        except Exception as e:
            print("hello", e)
            print("[Futurizing] %s" % path)
            try:
                os.system("futurize --stage1 -w %s" % path)
                with open(path) as f:
                    data = f.read()
                self.tree = ast.parse(data, path)
                self.script = jedi.Script(data, path=path, project=project)
            except:
                self.tree = None
                self.script = None
