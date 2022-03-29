def get_references_by_lineno(funcStats, script):
    """
    搜索所定义变量（右值为API Call）的所有引用处，还原引用处的API
    e.g. -> :
        dataset = tf.data.TFRecordDataset(...)
        dataset = dataset.batch(...)
        dataset = dataset.map(...)
        应该被还原为：
        tf.data.TFRecordDataset
        tf.data.TFRecordDataset.batch
        tf.data.TFRecordDataset.map
    """
    variables = funcStats["variables"]
    for i in range(len(variables)):  # 锁定第i个方法
        APIs_inFunc = funcStats["APIs"][i]  # 拿到第i个方法中所有的API
        check_table = funcStats["check_table"][i]
        for j in range(len(variables[i])):  # 锁定第i个方法中定义的第j个变量
            """
            variables[i][j] -> variable
            
            variables[i][j][0] -> lineno of variable
            variables[i][j][1] -> end_lineno of variable
            variables[i][j][2] -> col_offset of variable
            variables[i][j][3] -> end_col_offset of variable
            """
            references = script.get_references(line=variables[i][j][0], column=variables[i][j][2])
            for reference in references:
                if not reference.is_definition():
                    node_name = None
                    for check_item in check_table:
                        # 根据引用名去查表，得到结点全名；而且要求引用处所在行大于等于定义处
                        if reference.name == check_item[0] and reference.line >= check_item[2]:
                            node_name = check_item[1]
                            break  # 因为查找表没有去重，所以这里需要跳出循环
                        else:
                            continue
                    if node_name is not None:
                        """
                        `reference.name = node_name(...)`
                        The variable 'reference.name' is defined and the corresponding call 'node_name' is assigned to it
                        """
                        for api_sub in range(len(APIs_inFunc)):
                            targetStr = APIs_inFunc[api_sub].split('$')[0]  # obtain pure API without paras
                            if reference.name == targetStr.split('.')[0]:
                                tmp = targetStr.split('.')[1:]
                                new_name = ''
                                for name_seg in tmp:
                                    new_name += '.'
                                    new_name += name_seg
                                new_name = node_name + '.#' + new_name  # new_name after `#` is API inner_func
                                if check_item[1] == new_name:
                                    new_name = new_name + '.__call__'
                                if '$' in APIs_inFunc[api_sub]:
                                    paraLoc = APIs_inFunc[api_sub].find('$')
                                    paras = APIs_inFunc[api_sub][paraLoc:]
                                    new_name += paras
                                funcStats["APIs"][i][api_sub] = new_name
                            else:
                                continue
                    else:  # None of call nodes can match current variable
                        continue
                else:  # skip the definition of variable, what we need only is the references of variable defined
                    continue
    return funcStats
