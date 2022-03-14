import os
from pathlib import Path


def scan_two_sets(source, target):
    method_counter = 0
    sourceDict = {}
    for project in os.listdir(source):
        oneRepo = os.path.join(source, project)
        for path in Path(oneRepo).glob("./**/*.txt"):
            text = []
            with open(path) as f:
                for line in f:
                    if line != '' and line != '\n':
                        text.append(line)
            for i in range(len(text) - 1):
                if text[i].endswith(':\n') and not text[i + 1].endswith(':\n'):
                    method_counter += 1
            sourceDict[str(path)] = text
    targetDict = {}
    for project in os.listdir(target):
        oneRepo = os.path.join(target, project)
        for path in Path(oneRepo).glob("./**/*.txt"):
            text = []
            with open(path) as f:
                for line in f:
                    if line != '' and line != '\n':
                        text.append(line)
            for i in range(len(text) - 1):
                if text[i].endswith(':\n') and not text[i + 1].endswith(':\n'):
                    method_counter += 1
            targetDict[str(path)] = text
    for keyS, valueS in sourceDict.items():
        for keyT, valueT in targetDict.items():
            pathS = keyS.split('/')[-2:]
            pathT = keyT.split('/')[-2:]
            if pathS == pathT:
                for i in range(len(valueT)):
                    if not valueT[i].endswith(':\n'):
                        valueT[i] = (valueT[i]).split(' ')[0] + '\n'
                with open("/home/allen/DL_API/Static_Analysis/Python_Analyze/Intra_Method_Analysis/Resource/temp/check.txt", 'a+') as checker:
                    for itemS in valueS:
                        checker.write(itemS)
                    checker.write('-----\n')
                    for itemT in valueT:
                        checker.write(itemT)
                    checker.write('!!!!!\n\n')


def main():
    source = "/home/allen/DL_API/Static_Analysis/Python_Analyze/Intra_Method_Analysis/TestCaseSet"
    target = "/home/allen/DL_API/Static_Analysis/Python_Analyze/Intra_Method_Analysis/TestResult"
    scan_two_sets(source=source, target=target)


if __name__ == "__main__":
    main()
