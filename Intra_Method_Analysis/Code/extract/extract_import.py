import ast
from pprint import pprint

class ImportExtractor(ast.NodeVisitor):
    def __init__(self):
        self.filter = ["tensorflow", "numpy", "pandas", "sklearn", "pickle", "cv2", "keras"]
        self.stats = {
            "module": [],
            "source": [],
            "target": []
        }
        self.valid = {
            "module": [],
            "source": [],
            "target": []
        }

    def visit_Import(self, node):
        for alias in node.names:
            self.stats["module"].append(None)
            self.stats["source"].append(alias.name)
            if alias.asname is None:
                self.stats["target"].append(None)
            else:
                self.stats["target"].append(alias.asname)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.stats["module"].append(node.module)
            self.stats["source"].append(alias.name)
            if alias.asname is None:
                self.stats["target"].append(None)
            else:
                self.stats["target"].append(alias.asname)

    def report(self):
        pprint(self.valid)

    def getWanted(self):
        modules = self.stats["module"]
        sources = self.stats["source"]
        targets = self.stats["target"]
        for i in range(len(modules)):
            if modules[i] is None:  # Import
                source = sources[i].split('.')
                if source[0] in self.filter:
                    self.valid["module"].append(modules[i])
                    self.valid["source"].append(sources[i])
                    self.valid["target"].append(targets[i])
            else:  # ImportFrom
                module = modules[i].split('.')
                if module[0] in self.filter:
                    self.valid["module"].append(modules[i])
                    self.valid["source"].append(sources[i])
                    self.valid["target"].append(targets[i])
