import json


def chain_def_use(funcStats):
    """
    Case 1:
        ds = tf.data.Dataset.from_tensor_slices()
        ds = ds.repeat().shuffle().batch()
    """
    revert_table = open('/home/allen/DL_API/Static_Analysis/Python_Analyze/Intra_Method_Analysis/Resource/call_return.json', 'r+')
    revert_table = json.load(revert_table)
    for i in range(len(funcStats["name"])):
        for j in range(len(funcStats['APIs'][i])):
            cur_API = funcStats['APIs'][i][j]
            if cur_API is not None and '#' in cur_API:

                head = cur_API.split('#')[0][:-1]  # `API` or `API + Inner Func`
                rear = cur_API.split('#')[1][1:]
                possibleInnerFromHead = head.split('.')[-1]
                possibleAPIFromHead = '.'.join(head.split('.')[:-1])

                areYouOK = False

                for _, value in revert_table.items():
                    caller_User_API = value[0].split(',')[0][9:]
                    caller_Inner_Func = value[0].split(',')[1][11:]
                    callee_User_API = value[1].split(',')[0][9:]
                    # callee_Inner_Func = value[1].split(',')[1][11:]
                    if head == caller_User_API and rear == caller_Inner_Func:
                        result = callee_User_API
                        if rear != '':
                            result += ('.' + rear)
                        funcStats['APIs'][i][j] = result
                        areYouOK = True
                        break
                    elif possibleAPIFromHead == caller_User_API and possibleInnerFromHead == caller_Inner_Func:
                        result = callee_User_API
                        if rear != '':
                            result += ('.' + rear)
                        funcStats['APIs'][i][j] = result
                        areYouOK = True
                        break
                    else:
                        continue

                if not areYouOK:
                    result = head
                    if rear != '':
                        result += ('.' + rear)
                    funcStats['APIs'][i][j] = result
            else:
                continue
    return funcStats


def chain_sequence():
    """
    Case 2:
        X = tf.data.Dataset.from_tensor_slices().batch()
    """
    # TODO: complement it here or other place
    pass
