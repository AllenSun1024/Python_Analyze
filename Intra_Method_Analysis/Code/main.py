from Static_Analysis.Python_Analyze.Intra_Method_Analysis.Code.utils.scan_repo import scan_several_repos
import time


def main():
    """
    projects_path：你想要解析的代码仓库的路径
    scan_several_repos：扫描仓库中的每个项目
    """
    # projects_path = "/home/allen/DL_API/Static_Analysis/Python_Analyze/Intra_Method_Analysis/TestCaseSet"
    projects_path = "/home/allen/DL_API/Static_Analysis/sc_popular_star/home/fy/disk1/cjm/docker_data/pb_detect/projects/popular_star"
    scan_several_repos(projects_path)


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print("Time Elapsed: {}".format(end - start))
