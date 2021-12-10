import jedi
from pathlib import Path
from Intra_Method_Analysis.Code.utils.read_file import scan_one_file
from Intra_Method_Analysis.Code.extract.extract_import import ImportExtractor
from Intra_Method_Analysis.Code.extract.extract_funcDef import FuncDefExtractor
from Intra_Method_Analysis.Code.extract.jedi_search import get_references_by_lineno

def parse_tree_script(tree, script):
    """
    方法内API解析
    :param tree: Python AST
    :param script: Jedi Script
    import_extractor: 抽取并过滤import信息
    function_extractor: 抽取方法内API
    """


    import_extractor = ImportExtractor()
    import_extractor.generic_visit(tree)
    import_extractor.getWanted()
    # import_extractor.report()
    """
    validPackages:
    作用：存储当前文件被过滤后的import信息，用于包名还原
    结构：字典{'module': [...], 'source': [...], 'target': [...]}
    例子：{'module': [None, 'tensorflow.keras.layers'], 'source': ['tensorflow', 'Flatten'], 'target': ['tf', None]}
    """
    validPackages = import_extractor.valid


    function_extractor = FuncDefExtractor(script=script)
    function_extractor.generic_visit(tree)
    # funcStats = function_extractor.funcStats
    # get_references_by_lineno(funcStats=funcStats, script=script)
    # function_extractor.funcStats = revert_import_name(validPackages, funcStats)
    function_extractor.report()

def revert_import_name(validPackages, funcStats):
    for i in range(len(validPackages["module"])):
        """
        一个文件中存在多条import
        拿到第i条import信息A，B，C，去把对应的API拼接完整
        from A import B as C
        from A import B
        from A import *
        import B
        import B as C
        """
        A = validPackages["module"][i]
        B = validPackages["source"][i]
        C = validPackages["target"][i]
        for func_id in range(len(funcStats["name"])):
            """
            一个文件中存在多个函数
            拿到第func_id个函数，去拼接它的API
            """
            for api_id in range(len(funcStats["APIs"][func_id])):
                api_head = funcStats["APIs"][func_id][api_id].split('.')[0]
                if api_head == C:  # from A import B as C / import B as C
                    tmp = funcStats["APIs"][func_id][api_id].split('.')[1:]
                    result = ''
                    for item in tmp:
                        result += '.'
                        result += item
                    if A is None:  # import B as C
                        funcStats["APIs"][func_id][api_id] = B + result
                    else:  # from A import B as C
                        funcStats["APIs"][func_id][api_id] = A + '.' + B + result
                elif api_head == B:
                    if A is not None:  # from A import B
                        funcStats["APIs"][func_id][api_id] = A + '.' + funcStats["APIs"][func_id][api_id]
                else:
                    pass
    """
    过滤掉没有被选中的包
    过滤方式：将对应的API置为None，在extract_funcDef的report函数中输出最终结果时判断是否为None即可
    注意事项：问题1没有解决时就进行这一步，会导致API的遗漏
    """
    modules = []
    sources = []
    for module in validPackages["module"]:
        if module is not None:
            modules.append(module.split('.')[0])
    for source in validPackages["source"]:
        sources.append(source.split('.')[0])
    for func_id in range(len(funcStats["name"])):
        for api_id in range(len(funcStats["APIs"][func_id])):
            head = funcStats["APIs"][func_id][api_id].split('.')[0]
            if head not in modules and head not in sources and head not in validPackages["module"] and head not in validPackages["source"] and '*' not in validPackages["source"]:
                funcStats["APIs"][func_id][api_id] = None
    return funcStats

def extract_one_repo(project_path):  # 解析一个项目
    project = jedi.Project(path=project_path)
    for f in Path(project_path).glob("./**/*.py"):
        tree, script = scan_one_file(f, project)
        if not tree or not script:
            print("[Error] Failed to parse file: %s" % str(f))
            continue
        else:
            parse_tree_script(tree, script)
