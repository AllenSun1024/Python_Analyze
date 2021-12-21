from Intra_Method_Analysis.Code.utils.scan_repo import scan_several_repos


def main():
    """
    projects_path：你想要解析的代码仓库的路径
    scan_several_repos：扫描仓库中的每个项目
    """
    projects_path = "/home/allen/DL_API/Static_Analysis/Python_Analyze/Intra_Method_Analysis/TestCaseSet"
    scan_several_repos(projects_path)


if __name__ == '__main__':
    main()
