'''
题目
难度：★☆☆☆☆
类型：数组

给定一个由整数组成的非空数组所表示的非负整数，在该数的基础上加一。

最高位数字存放在数组的首位， 数组中每个元素只存储一个数字。

你可以假设除了整数 0 之外，这个整数不会以零开头。

示例
示例 1:

输入: [1,2,3]
输出: [1,2,4]
解释: 输入数组表示数字 123。
示例 2:

输入: [4,3,2,1]
输出: [4,3,2,2]
解释: 输入数组表示数字 4321。
'''


def list_add(n):
    n[-1] += 1
    if n[-1] > 9:
        n[-2] += 1
        n[-1] -= 10
    return n


print(list_add([1, 2, 9]))

# 另外的解法
a = [1, 2, 9]
print(list(map(int, str(int(''.join(map(str, a))) + 1))))
