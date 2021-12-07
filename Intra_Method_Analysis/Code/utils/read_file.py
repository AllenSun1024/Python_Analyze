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
        except Exception as e:  # convert py2 to py3
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


def scan_one_file(path, project):  # scan some python file in the project
    print("[Scanning] %s" % str(path))
    file_data = GetProject(path, project)
    tree = file_data.tree
    script = file_data.script
    return tree, script
