
'''
字典解压,x.y.z 的意思是x里嵌套了y y里嵌套了z
dict1 = {'A': 1, 'B.A': 2, 'B.B': 3, 'CC.D.E': 4, 'CC.D.F': 5}
解压成：{'A': 1, 'B': {'A': 2, 'B': 3}, 'CC': {'D': {'E': 4, 'F': 5}}}
'''



dict1 = {'A': 1, 'B.A': 2, 'B.B': 3, 'CC.D.E': 4, 'CC.D.F': 5}

# 字符串转字典方法
def func(dic):
    result = dict()
    for key, value in dic.items():
        keys = str(key).upper().split('.')
        test = 'result'
        li = [r"['%s']" % e_key for e_key in keys]
        last = li.pop()
        for i in li:
            test += i
            try:
                eval(test)
            except KeyError:
                exec(test + '= dict()')
        test += last
        test += r'= %d' % value
        exec(test)
    return result


def flatten(dict1):
    dict2 = dict()
    for key,value in dict1.items():
        keys = str(key).upper().split('.')

        def deepSearch(dict1, dict2):
            for key in dict2.keys():
                if key not in dict1.keys():
                    dict1[key] = dict2[key]
                else:
                    deepSearch(dict1[key], dict2[key])

        dd = {}
        for i, k in enumerate(keys[::-1]):
            if i == 0:
                dd[k] = value
            else:
                dd = {k: dd.copy()}

        deepSearch(dict2,dd)

    return dict2

print(flatten(dict1))
