from pathlib import Path
import os


def main():
    projectPath = "/home/allen/DL_API/Static_Analysis/sc_popular_star/home/fy/disk1/cjm/docker_data/pb_detect/projects/popular_star"
    fileCounter = 0
    for f in Path(projectPath).glob("./**/*.py"):
        fileCounter += 1
    print("Num of python files: %d" % fileCounter)
    dirCounter = 0
    valiDirCounter = 0
    for d in os.listdir(projectPath):
        dirCounter += 1
        projectName = (str(d)).lower()
        if 'example' not in projectName and 'tutorial' not in projectName:
            valiDirCounter += 1
    print("Num of projects: %d" % dirCounter)
    print("Num of valid projects: %d" % valiDirCounter)


if __name__ == '__main__':
    main()
