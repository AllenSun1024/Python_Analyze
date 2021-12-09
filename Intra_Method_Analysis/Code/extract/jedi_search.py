def get_references_by_lineno(funcStats, script):
    APIs = funcStats["APIs"]
    lineNos = funcStats["lineNo"]
    colNos = funcStats["columnNo"]
    for i in range(len(lineNos)):
        for j in range(len(lineNos[i])):
            print(APIs[i][j], ':')
            result = script.get_references(line=lineNos[i][j], column=colNos[i][j]-3)
            for item in result:
                if not item.is_definition():
                    print(item)
        print('\n')
