import jedi
from pathlib import Path
from Intra_Method_Analysis.Code.utils.read_file import scan_one_file
from Intra_Method_Analysis.Code.extract.extract_import import ImportExtractor
from Intra_Method_Analysis.Code.extract.extract_funcDef import FuncDefExtractor

def parse_tree_script(tree, script):
    import_extractor = ImportExtractor()
    import_extractor.generic_visit(tree)
    import_extractor.getWanted()
    import_extractor.report()


def extract_one_repo(project_path):
    project = jedi.Project(path=project_path)
    for f in Path(project_path).glob("./**/*.py"):
        tree, script = scan_one_file(f, project)
        if not tree or not script:
            print("[Error] Failed to parse file: %s" % str(f))
            continue
        else:
            parse_tree_script(tree, script)
