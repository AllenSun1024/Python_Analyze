import ast
from pprint import pprint

class ImportExtractor(ast.NodeVisitor):
    """
    import tensorflow as XXX
    from tensorflow import YYY, ZZZ as y, z
    """
    def __init__(self):
        self.package = "tensorflow"
        self.as_name_import = []  # XXX
        self.name_import_from = []  # YYY, ZZZ
        self.as_name_import_from = []  # y, z

    def visit_Import(self, node):
        for curNode in node.names:
            if curNode.name == self.package:
                self.as_name_import.append(curNode.asname)

    def visit_ImportFrom(self, node):
        if node.module == "tensorflow":
            for curNode in node.names:
                self.name_import_from.append(curNode.name)
                self.as_name_import_from.append(curNode.asname)

    def report(self):
        pprint(self.as_name_import)
        pprint(self.name_import_from)
        pprint(self.as_name_import_from)
