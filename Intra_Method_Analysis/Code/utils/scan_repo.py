import os
from Intra_Method_Analysis.Code.extract.analyze_file import extract_one_repo

def scan_several_repos(root_path):
    for project in os.listdir(root_path):
        extract_one_repo(os.path.join(root_path, project))
