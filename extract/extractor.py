import jedi
from pathlib import Path
from utils.scanFile import scan_one_file
from extract.importFilter import ImportFilter
from extract.functionDefFinder import FunctionDefFinder

def tf_api_match(valid_import, intra_func_api):
    result = []
    for item in intra_func_api:
        tmp = []
        for api in item:
            cur = api.split('.')
            if cur[0] in valid_import:
                tmp.append(api)
        result.append(tmp)
    return result

def write_results(result, path):
    with open("result.txt", 'a') as f:
        f.write(str(path))
        f.write('\n')
        for i, item in enumerate(result):
            f.write('function-')
            f.write(str(i+1))
            f.write('\n')
            for cur in item:
                f.write(cur)
            f.write('\n')
        f.write('\n')
        f.close()

def parse_single_repo(project_path):
    project = jedi.Project(path=project_path)
    counter = 0
    for f in Path(project_path).glob("./**/*.py"):
        tree, script = scan_one_file(f, project)
        if not tree or not script:
            print("[Error] failed to read the file %s" % str(f))
            continue
        import_finder = ImportFilter()
        import_finder.generic_visit(tree)
        valid_import = ["tensorflow"] + import_finder.as_name_import + import_finder.as_name_import_from + import_finder.name_import_from
        func_def_finder = FunctionDefFinder()
        func_def_finder.generic_visit(tree)
        intra_func_api = func_def_finder.eachFunc
        result = tf_api_match(valid_import, intra_func_api)
        write_results(result, f)
        counter += 1
        if counter >= 3:
            break

