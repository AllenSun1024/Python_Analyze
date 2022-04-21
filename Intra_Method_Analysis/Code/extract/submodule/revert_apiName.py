import json


def revert_import_name(validPackages, funcStats):
    """
    根据import信息，将抽取出来的API名称完整还原
    e.g., tf.data.from_tensor_slices -> tensorflow.data.from_tensor_slices
    :param validPackages: 过滤后的import信息
    :param funcStats: 当前文件中，所有函数的API信息
    :return: 具有完整名称的API信息
    """
    for func_id in range(len(funcStats["name"])):
        """
        一个文件中存在多个函数
        拿到第func_id个函数，去拼接它的API
        """
        for api_id in range(len(funcStats["APIs"][func_id])):
            if funcStats["APIs"][func_id][api_id] is None:
                continue
            if '$' in funcStats["APIs"][func_id][api_id]:
                pureAPI = funcStats["APIs"][func_id][api_id].split('$')[0]
                pureAPIName = _revert_pureAPI_name(validPackages=validPackages, pureAPI=pureAPI)
                paraList = funcStats["APIs"][func_id][api_id].split('$')[1:]
                paraName = _revert_para_name(validPackages=validPackages, paraList=paraList)
                funcStats["APIs"][func_id][api_id] = pureAPIName + paraName
            else:
                pureAPIName = _revert_pureAPI_name(validPackages=validPackages,
                                                   pureAPI=funcStats["APIs"][func_id][api_id])
                funcStats["APIs"][func_id][api_id] = pureAPIName

    """
    过滤掉没有被选中的包
    过滤方式：将对应的API置为None，在extract_funcDef的report函数中输出最终结果时判断是否为None即可
    """
    modules = []
    sources = []
    for module in validPackages["module"]:
        if module is not None:
            modules.append(module.split('.')[0])
    for source in validPackages["source"]:
        sources.append(source.split('.')[0])
    for func_id in range(len(funcStats["name"])):
        for api_id in range(len(funcStats["APIs"][func_id])):
            if funcStats["APIs"][func_id][api_id] is None:
                continue
            head = funcStats["APIs"][func_id][api_id].split('.')[0]
            if head not in modules and head not in sources and head not in validPackages["module"] and head not in validPackages["source"]:
                funcStats["APIs"][func_id][api_id] = None
    return funcStats


def _revert_para_name(validPackages, paraList):
    resultList = []
    for para in paraList:
        paraHead = para.split('.')[0]
        leftArg = ''
        if '=' in paraHead:
            leftArg = paraHead.split('=')[0]
            paraHead = paraHead.split('=')[1]
        paraBody = para.split('.')[1:]
        for i in range(len(validPackages["module"])):
            A = validPackages["module"][i]
            B = validPackages["source"][i]
            C = validPackages["target"][i]
            """
            一个文件中存在多条import
            拿到第i条import信息A，B，C，去把对应的API拼接完整
            from A import B as C
            from A import B
            from A import *
            import B
            import B as C
            """
            if paraHead == C:  # from A import B as C `or` import B as C
                paraBodyName = ''
                for body in paraBody:
                    paraBodyName += ('.' + body)
                paraName = B + paraBodyName
                if A is not None:
                    paraName = A + '.' + paraName
                if leftArg != '':
                    paraName = leftArg + '=' + paraName
                resultList.append(paraName)
                break
            elif paraHead == B:  # from A import B `or` import B
                paraName = para
                if A is not None:
                    paraName = A + '.' + paraName
                if leftArg != '':
                    paraName = leftArg + '=' + paraName
                resultList.append(paraName)
                break
            else:
                if A is not None and B == '*':  # from A import *
                    with open(
                            '/home/allen/DL_API/Static_Analysis/Python_Analyze/Intra_Method_Analysis/Resource/module_check.json') as json_file:
                        module_check_table = json.load(json_file)
                        json_file.close()
                    if A in module_check_table.keys() and paraHead in module_check_table[A]:
                        paraName = A + '.' + para
                        if leftArg != '':
                            paraName = leftArg + '=' + paraName
                        resultList.append(paraName)
                        break
    """
    过滤掉没有被选中的包
    """
    modules = []
    sources = []
    for module in validPackages["module"]:
        if module is not None:
            modules.append(module.split('.')[0])
    for source in validPackages["source"]:
        sources.append(source.split('.')[0])
    validResult = []
    for api in resultList:
        apiHead = ''
        if '=' in api:
            apiHead = api.split('=')[1]
            apiHead = apiHead.split('.')[0]
        else:
            apiHead = api.split('.')[0]
        if apiHead in modules or apiHead in sources or apiHead in validPackages["module"] or apiHead in \
                validPackages["source"]:
            validResult.append(api)
    finalResultString = ''
    if validResult:
        for validAPI in validResult:
            finalResultString += ('$' + validAPI)
    return finalResultString


def _revert_pureAPI_name(validPackages, pureAPI):  # pureAPI means `API which does not contain $`
    apiHead = pureAPI.split('.')[0]
    apiBody = pureAPI.split('.')[1:]
    finalName = ''
    for i in range(len(validPackages["module"])):
        A = validPackages["module"][i]
        B = validPackages["source"][i]
        C = validPackages["target"][i]
        """
        一个文件中存在多条import
        拿到第i条import信息A，B，C，去把对应的API拼接完整
        from A import B as C
        from A import B
        from A import *
        import B
        import B as C
        """
        if apiHead == C:  # from A import B as C `or` import B as C
            apiBodyName = ''
            for body in apiBody:
                apiBodyName += ('.' + body)
            apiName = B + apiBodyName
            if A is not None:
                apiName = A + '.' + apiName
            finalName = apiName
        elif apiHead == B:  # from A import B `or` import B
            apiName = pureAPI
            if A is not None:
                apiName = A + '.' + apiName
            finalName = apiName
        else:
            if A is not None and B == '*':  # from A import *
                with open(
                        '/home/allen/DL_API/Static_Analysis/Python_Analyze/Intra_Method_Analysis/Resource/module_check.json') as json_file:
                    module_check_table = json.load(json_file)
                    json_file.close()
                if A in module_check_table.keys() and apiHead in module_check_table[A]:
                    apiName = A + '.' + pureAPI
                    finalName = apiName
    if finalName != '':
        """
        过滤掉没有被选中的包
        """
        modules = []
        sources = []
        for module in validPackages["module"]:
            if module is not None:
                modules.append(module.split('.')[0])
        for source in validPackages["source"]:
            sources.append(source.split('.')[0])
        validHead = finalName.split('.')[0]
        if validHead not in modules and validHead not in sources and validHead not in validPackages["module"] and validHead not in validPackages["source"]:
            finalName = ''
    return finalName
