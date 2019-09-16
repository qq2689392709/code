'''
题目
难度：★☆☆☆☆
类型：数组

给定一个非负整数 numRows，生成杨辉三角的前 *numRows *行。

在杨辉三角中，每个数是它左上方和右上方的数的和。
'''


def createL(l):  # 生成杨辉三角的一行
    L = [1]
    for x in range(1, len(l)):
        L.append(l[x] + l[x - 1])
    L.append(1)
    return L


def printL(L, W):  # 打印
    s = ""
    for x in L:
        s += str(x) + "  "
    print(s.center(W))


L = [1]
row = int(input("输入行数："))
width = row * 4  # 设置打印宽度
for x in range(row):
    printL(L, width)
    L = createL(L)
