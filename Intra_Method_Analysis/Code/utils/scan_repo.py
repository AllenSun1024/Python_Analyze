import os
from Intra_Method_Analysis.Code.extract.analyze_file import extract_one_repo


def scan_several_repos(root_path):
    """
    解析仓库中的所有项目
    :param root_path: 仓库路径
    """
    for project in os.listdir(root_path):
        extract_one_repo(os.path.join(root_path, project))
