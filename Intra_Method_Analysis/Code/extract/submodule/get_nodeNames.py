import ast


def go_back(node):
    """
    回溯找到切割点
    """
    if isinstance(node, ast.Call):  # 确保就是Call结点
        if isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name):
                return node.func.value
            elif isinstance(node.func.value, ast.Call):
                return go_back(node.func.value)
            elif isinstance(node.func.value, ast.Attribute):
                return node.func.value
            else:
                return node.func
        else:
            return node.func  # 为了程序的鲁棒，调用者拿到返回值后应该判断node.func的类型
    else:
        return None


def get_Call_Name(node, name):
    """
    根据API中各结点的类型，递归拼接出API完整、合理的名字
    """
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Call):
            call_breakpoint = go_back(node.func.value)
            if call_breakpoint is None:
                # 遇到尚未考虑到的特殊语法结构，就停止递归，返回可能不完整的API名称，我们选择直接抛弃
                # 此处会导致风险，但不会使程序崩溃
                return None
            else:
                if call_breakpoint != node.func.value.func:
                    name = node.func.attr + '.' + name
                else:
                    pass
                if isinstance(call_breakpoint, ast.Name) or isinstance(call_breakpoint, ast.Attribute):
                    return get_Call_Name(call_breakpoint, name)
                else:
                    return None
        elif isinstance(node.func, ast.Call):
            # TODO: only able to handle A()() correctly, need APIs' return values to be more precise
            name = name + '__call__.'
            return get_Call_Name(node.func, name)
        else:
            return get_Call_Name(node.func, name)
    elif isinstance(node, ast.Attribute):
        name = node.attr + '.' + name
        return get_Call_Name(node.value, name)
    elif isinstance(node, ast.Name):
        return node.id + '.' + name  # 递归出口
    else:
        return None


def get_Attribute_Name(node, name):
    """
    node is an Attribute Node in AST
    """
    name = '.' + node.attr + name
    if isinstance(node.value, ast.Name):
        name = node.value.id + name
        return name
    elif isinstance(node.value, ast.Attribute):
        return get_Attribute_Name(node.value, name)
    else:
        pass
