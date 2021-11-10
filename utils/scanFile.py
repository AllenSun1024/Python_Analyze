from utils.getDataFromFile import GetDataFromFile

def scan_one_file(f, project):
    print("[Scanning] %s" % str(f))
    file_data = GetDataFromFile(f, project)
    tree = file_data.tree
    script = file_data.script
    return tree, script