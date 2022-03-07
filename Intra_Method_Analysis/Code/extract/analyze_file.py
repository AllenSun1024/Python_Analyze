import jedi
from pathlib import Path
from Static_Analysis.Python_Analyze.Intra_Method_Analysis.Code.utils.read_file import scan_one_file
from Static_Analysis.Python_Analyze.Intra_Method_Analysis.Code.extract.extract_import import ImportExtractor
from Static_Analysis.Python_Analyze.Intra_Method_Analysis.Code.extract.extract_funcDef import FuncDefExtractor
from Static_Analysis.Python_Analyze.Intra_Method_Analysis.Code.extract.submodule.search_variableReference import get_references_by_lineno
from Static_Analysis.Python_Analyze.Intra_Method_Analysis.Code.extract.submodule.revert_apiName import revert_import_name
from Static_Analysis.Python_Analyze.Intra_Method_Analysis.Code.extract.submodule.revert_call_chain import chain_def_use


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
    import_extractor.module_Filter()
    """
    validPackages:
    作用：存储当前文件被过滤后的import信息，用于包名还原
    结构：字典{'module': [...], 'source': [...], 'target': [...]}
    例子：{'module': [None, 'tensorflow.keras.layers'], 'source': ['tensorflow', 'Flatten'], 'target': ['tf', None]}
    """
    validPackages = import_extractor.valid

    function_extractor = FuncDefExtractor(script=script)
    function_extractor.generic_visit(tree)
    funcStats = function_extractor.funcStats
    funcStats = get_references_by_lineno(funcStats=funcStats, script=script)
    function_extractor.funcStats = revert_import_name(validPackages, funcStats)
    function_extractor.funcStats = chain_def_use(funcStats=function_extractor.funcStats)
    function_extractor.report()


def extract_one_repo(project_path):
    """
    解析一个项目
    :param project_path: 当前项目路径
    """
    project = jedi.Project(path=project_path)
    for f in Path(project_path).glob("./**/*.py"):
        tree, script = scan_one_file(f, project)
        if not tree or not script:
            print("[Error] Failed to parse file: %s" % str(f))
            continue
        else:
            parse_tree_script(tree, script)
