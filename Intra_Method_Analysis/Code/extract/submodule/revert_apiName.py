import json


def revert_import_name(validPackages, funcStats):
    """
    根据import信息，将抽取出来的API名称完整还原
    e.g., tf.data.from_tensor_slices -> tensorflow.data.from_tensor_slices
    :param validPackages: 过滤后的import信息
    :param funcStats: 当前文件中，所有函数的API信息
    :return: 具有完整名称的API信息
    """
    for i in range(len(validPackages["module"])):
        """
        一个文件中存在多条import
        拿到第i条import信息A，B，C，去把对应的API拼接完整
        from A import B as C
        from A import B
        from A import *
        import B
        import B as C
        """
        A = validPackages["module"][i]
        B = validPackages["source"][i]
        C = validPackages["target"][i]
        for func_id in range(len(funcStats["name"])):
            """
            一个文件中存在多个函数
            拿到第func_id个函数，去拼接它的API
            """
            for api_id in range(len(funcStats["APIs"][func_id])):
                pureAPI = ''
                if funcStats["APIs"][func_id][api_id] is not None:
                    pureAPI = funcStats["APIs"][func_id][api_id].split('$')[0]  # API without Paras
                api_head = pureAPI.split('.')[0]
                if api_head == C:  # from A import B as C / import B as C
                    tmp = pureAPI.split('.')[1:]
                    result = ''
                    for item in tmp:
                        result += '.'
                        result += item
                    if A is None:  # import B as C
                        if '$' not in funcStats["APIs"][func_id][api_id]:
                            funcStats["APIs"][func_id][api_id] = B + result
                        else:
                            paraList = funcStats["APIs"][func_id][api_id].split('$')[1:]
                            validParas = _revert_para_API(validPackages=validPackages, paraList=paraList)
                            funcStats["APIs"][func_id][api_id] = B + result + validParas
                    else:  # from A import B as C
                        if '$' not in funcStats["APIs"][func_id][api_id]:
                            funcStats["APIs"][func_id][api_id] = A + '.' + B + result
                        else:
                            paraList = funcStats["APIs"][func_id][api_id].split('$')[1:]
                            validParas = _revert_para_API(validPackages=validPackages, paraList=paraList)
                            funcStats["APIs"][func_id][api_id] = A + '.' + B + result + validParas
                elif api_head == B:
                    if A is not None:  # from A import B
                        if '$' not in funcStats["APIs"][func_id][api_id]:
                            funcStats["APIs"][func_id][api_id] = A + '.' + funcStats["APIs"][func_id][api_id]
                        else:
                            paraList = funcStats["APIs"][func_id][api_id].split('$')[1:]
                            validParas = _revert_para_API(validPackages=validPackages, paraList=paraList)
                            funcStats["APIs"][func_id][api_id] = A + '.' + pureAPI + validParas
                    else:  # import B
                        if '$' not in funcStats["APIs"][func_id][api_id]:
                            continue
                        else:
                            paraList = funcStats["APIs"][func_id][api_id].split('$')[1:]
                            validParas = _revert_para_API(validPackages=validPackages, paraList=paraList)
                            funcStats["APIs"][func_id][api_id] = pureAPI + validParas
                else:
                    if A is not None and B == '*':  # from A import *
                        with open('/home/allen/DL_API/Static_Analysis/Python_Analyze/Intra_Method_Analysis/Resource/module_check.json') as json_file:
                            module_check_table = json.load(json_file)
                        if A in module_check_table.keys() and api_head in module_check_table[A]:
                            if '$' not in funcStats["APIs"][func_id][api_id]:
                                funcStats["APIs"][func_id][api_id] = A + '.' + funcStats["APIs"][func_id][api_id]
                            else:
                                paraList = funcStats["APIs"][func_id][api_id].split('$')[1:]
                                validParas = _revert_para_API(validPackages=validPackages, paraList=paraList)
                                funcStats["APIs"][func_id][api_id] = A + '.' + pureAPI + validParas
                        else:
                            continue
                    else:
                        continue
    """
    过滤掉没有被选中的包
    过滤方式：将对应的API置为None，在extract_funcDef的report函数中输出最终结果时判断是否为None即可
    """
    modules = []
    sources = []
    for module in validPackages["module"]:
        if module is not None:
            modules.append(module.split('.')[0])
        else:
            continue
    for source in validPackages["source"]:
        sources.append(source.split('.')[0])
    for func_id in range(len(funcStats["name"])):
        for api_id in range(len(funcStats["APIs"][func_id])):
            head = ''
            if funcStats["APIs"][func_id][api_id] is not None:
                head = funcStats["APIs"][func_id][api_id].split('.')[0]
            if head not in modules and head not in sources and head not in validPackages["module"] and head not in \
                    validPackages["source"]:
                funcStats["APIs"][func_id][api_id] = None
            else:
                continue
    return funcStats


def _revert_para_API(validPackages, paraList):
    validParas = []
    for i in range(len(validPackages["module"])):
        """
        一个文件中存在多条import
        拿到第i条import信息A，B，C，去把对应的API拼接完整
        from A import B as C
        from A import B
        from A import *
        import B
        import B as C
        """
        A = validPackages["module"][i]
        B = validPackages["source"][i]
        C = validPackages["target"][i]
        for para in paraList:
            api_head = para.split('.')[0]
            if api_head == C:  # from A import B as C / import B as C
                tmp = para.split('.')[1:]
                result = ''
                for item in tmp:
                    result += '.'
                    result += item
                if A is None:  # import B as C
                    validParas.append(B + result)
                else:  # from A import B as C
                    validParas.append(A + '.' + B + result)
            elif api_head == B:
                if A is not None:  # from A import B
                    validParas.append(A + '.' + para)
                else:  # import B
                    continue
            else:
                if A is not None and B == '*':  # from A import *
                    with open(
                            '/home/allen/DL_API/Static_Analysis/Python_Analyze/Intra_Method_Analysis/Resource/module_check.json') as json_file:
                        module_check_table = json.load(json_file)
                    if A in module_check_table.keys() and api_head in module_check_table[A]:
                        validParas.append(A + '.' + para)
                    else:
                        continue
                else:
                    continue
    modules = []
    sources = []
    for module in validPackages["module"]:
        if module is not None:
            modules.append(module.split('.')[0])
        else:
            continue
    for source in validPackages["source"]:
        sources.append(source.split('.')[0])
    parasFiltered = []
    for para in validParas:
        head = para.split('.')[0]
        if head not in modules and head not in sources and head not in validPackages["module"] and head not in \
                validPackages["source"]:
            continue
        else:
            parasFiltered.append(para)
    finalResult = ''
    for para in parasFiltered:
        finalResult += ('$' + para)
    return finalResult
