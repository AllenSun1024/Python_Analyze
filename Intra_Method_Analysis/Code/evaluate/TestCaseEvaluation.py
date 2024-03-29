import os
from pathlib import Path


def scan_two_sets(source, target):
    method_counter_1 = 0
    method_counter_2 = 0
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
                    method_counter_1 += 1
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
                    method_counter_2 += 1
            targetDict[str(path)] = text
    counter = 0
    validData = []
    validPath = []
    for keyS, valueS in sourceDict.items():
        dataS = []
        for i, item in enumerate(valueS):
            if item.endswith(':\n'):
                if i < len(valueS) - 1 and not valueS[i + 1].endswith(':\n'):
                    curS = ''
                    start = i + 1
                    if '/' in item:
                        curS = (item.split('/'))[1]
                    else:
                        curS = item
                    while start < len(valueS) and not valueS[start].endswith(':\n'):
                        curS += valueS[start]
                        start += 1
                    dataS.append(curS)
                else:
                    continue
            else:
                continue
        for keyT, valueT in targetDict.items():
            pathS = keyS.split('/')[-2:]
            pathT = keyT.split('/')[-2:]
            if pathS == pathT:
                for i in range(len(valueT)):
                    if not valueT[i].endswith(':\n'):
                        valueT[i] = (valueT[i]).split(' ')[0] + '\n'
                dataT = []
                for i, item in enumerate(valueT):
                    if item.endswith(':\n'):
                        if i < len(valueT) - 1 and not valueT[i + 1].endswith(':\n'):
                            curT = ''
                            start = i + 1
                            if '/' in item:
                                curT = (item.split('/'))[1]
                            else:
                                curT = item
                            while start < len(valueT) and not valueT[start].endswith(':\n'):
                                curT += valueT[start]
                                start += 1
                            dataT.append(curT)
                        else:
                            continue
                    else:
                        continue
                for dS in dataS:
                    for dT in dataT:
                        if dS == dT:
                            counter += 1
                            validPath.append(pathS)
                            validData.append(dS)
    print("Num of Methods: {}".format(method_counter_2))
    print("Equal: {}".format(counter))
    with open("/home/allen/DL_API/Static_Analysis/Python_Analyze/Intra_Method_Analysis/Resource/temp/paths.txt", "a+") as f:
        pathsEncountered = set()
        for p in validPath:
            pathsEncountered.add((p[0] + '  ' + p[1]))
        temp = []
        for p in pathsEncountered:
            temp.append(p)
        temp.sort()
        for item in temp:
            f.write(item)
            f.write('\n')
        f.close()


def main():
    source = "/home/allen/DL_API/Static_Analysis/Python_Analyze/Intra_Method_Analysis/TestCaseSet"
    target = "/home/allen/DL_API/Static_Analysis/Python_Analyze/Intra_Method_Analysis/TestResult"
    scan_two_sets(source=source, target=target)


if __name__ == "__main__":
    main()
