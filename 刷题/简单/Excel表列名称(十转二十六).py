'''
题目
难度：★☆☆☆☆
类型：数学

给定一个正整数，返回它在 Excel 表中相对应的列名称。

例如，

1 -> A
2 -> B
3 -> C
...
26 -> Z
27 -> AA
28 -> AB
...
示例
示例 1:
输入: 1
输出: "A"

示例 2:

输入: 28
输出: "AB"

示例 3:
输入: 701
输出: "ZY"
'''


def shi_AZ(n):
    res = ''
    while n:
        n -= 1
        n, r = n // 26, n % 26
        res = chr(65 + r) + res
    return res


print(shi_AZ(1))
print(shi_AZ(28))
print(shi_AZ(701))
