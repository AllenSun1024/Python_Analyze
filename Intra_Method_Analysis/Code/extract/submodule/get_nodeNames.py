import ast


def go_back(node):  # node is ast.Call
    """
    回溯找到切割点
    """
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
        return node.func


def get_Call_Name(node, name):
    """
    根据API中各结点的类型，递归拼接出API完整、合理的名字
    """
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Call):
            if go_back(node.func.value) != node.func.value.func:
                name = node.func.attr + '.' + name
            return get_Call_Name(go_back(node.func.value), name)
        else:
            return get_Call_Name(node.func, name)
    elif isinstance(node, ast.Attribute):
        name = node.attr + '.' + name
        return get_Call_Name(node.value, name)
    elif isinstance(node, ast.Name):
        return node.id + '.' + name  # 递归出口
    elif isinstance(node, ast.Subscript):
        return get_Call_Name(node.value, name)
    else:
        return None
