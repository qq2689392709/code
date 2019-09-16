'''
题目
难度：★☆☆☆☆
类型：数学

判断一个整数是否是回文数。回文数是指正序（从左向右）和倒序（从右向左）读都是一样的整数。

示例
示例 1:

输入: 121
输出: true

示例 2:
输入: -121
输出: false
解释: 从左向右读, 为 -121 。 从右向左读, 为 121- 。因此它不是一个回文数。

示例 3:
输入: 10
输出: false
解释: 从右向左读, 为 01 。因此它不是一个回文数。

进阶:
你能不将整数转为字符串来解决这个问题吗？
'''


def palindromic(n):
    n = str(n)
    return n == n[::-1]


print(palindromic('121'))
print(palindromic('-121'))
print(palindromic('10'))


# 进阶，取余
def palindromic2(n):
    c = 0  # 统计位数
    n1 = n  # 浅拷贝一份
    while n1 != 0:  # 计算几位数
        n1 = n1 // 10
        c += 1
    # 对各个位数进行整除后取余后生成列表
    num_list = [n // (10 ** (c - x)) % 10 for x in range(1, c + 1)]
    return num_list == num_list[::-1]


print(palindromic2(12321))
