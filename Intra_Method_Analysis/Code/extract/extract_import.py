import ast
from pprint import pprint


class ImportExtractor(ast.NodeVisitor):
    def __init__(self):
        """
        :param: self.filter，需要被解析的第三方包在此处注册包名，否则会被抛弃
        :param: self.stats，记录当前文件中的全部import信息
        :param: self.valid，self.stats经过self.filter包名过滤后的结果
        """
        # self.filter = ["tensorflow", "numpy", "pandas", "sklearn", "pickle", "cv2", "keras"]
        self.filter = ["tensorflow", "keras"]
        """
        from module import source as target
        e.g., "from tensorflow import keras as k": module->tensorflow, source->keras, target->k
        e.g., "from tensorflow import *": module->tensorflow, source->*, target->None
        e.g., "import tensorflow as tf": module->None, source->tensorflow, target->tf
        e.g., "import tensorflow": module->None, source->tensorflow, target->None
        e.g., "from tensorflow import keras, nn" will be parsed like: "from tensorflow import keras" and "from tensorflow import nn"
        """
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
            if alias.asname is None:  # import B
                self.stats["target"].append(None)
            else:  # import B as C
                self.stats["target"].append(alias.asname)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.stats["module"].append(node.module)
            self.stats["source"].append(alias.name)
            if alias.asname is None:  # from A import B
                self.stats["target"].append(None)
            else:  # from A import B as C
                self.stats["target"].append(alias.asname)

    def report(self):
        """
        供debug时打印数据
        """
        pprint(self.valid)

    def module_Filter(self):
        """
        基于self.filter，过滤出想要解析的模块
        """
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
                else:
                    continue
            else:  # ImportFrom
                module = modules[i].split('.')
                if module[0] in self.filter:
                    self.valid["module"].append(modules[i])
                    self.valid["source"].append(sources[i])
                    self.valid["target"].append(targets[i])
                else:
                    continue
