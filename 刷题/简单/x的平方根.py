'''
题目
难度：★★☆☆☆
类型：数组

实现 int sqrt(int x) 函数。

计算并返回 x 的平方根，其中 x 是非负整数。

由于返回类型是整数，结果只保留整数的部分，小数部分将被舍去。

示例
示例 1:

输入: 4
输出: 2
示例 2:

输入: 8
输出: 2
说明: 8 的平方根是 2.82842...,
由于返回类型是整数，小数部分将被舍去。
'''


# int(x**0.5)
def int_sqrt(n):
    return int(n ** 0.5)


print(int_sqrt(4))
print(int_sqrt(8))


# 二分法

def sqrt(x):
    low = 0
    mid = x // 2
    high = x
    while low <= high:  # 注意判断条件
        if mid * mid > x:
            high = mid - 1
        elif mid * mid < x:
            low = mid + 1
        else:
            return mid
        mid = (low + high) // 2
    return mid  # 向下取整
