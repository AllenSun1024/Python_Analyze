def parse_function_arguments(node):
    """
    在函数定义处获取其形式参数
    :param node: 函数定义结点ast.FunctionDef
    :return: 函数定义时声明的形式参数列表
    """
    args = []
    if node.args.posonlyargs is not None:
        for arg in node.args.posonlyargs:
            args.append(arg.arg)
    else:
        pass
    if node.args.args is not None:
        for arg in node.args.args:
            args.append(arg.arg)
    else:
        pass
    if node.args.kwonlyargs:
        for arg in node.args.kwonlyargs:
            args.append(arg.arg)
    else:
        pass
    if node.args.vararg is not None:
        args.append(node.args.vararg.arg)
    else:
        pass
    if node.args.kwarg is not None:
        args.append(node.args.kwarg.arg)
    else:
        pass
    return args
