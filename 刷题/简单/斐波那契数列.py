'''
题目
难度：★☆☆☆☆
类型：数学

斐波那契数，通常用 F(n) 表示，形成的序列称为斐波那契数列。该数列由 0 和 1 开始，后面的每一项数字都是前面两项数字的和。也就是：

F(0) = 0, F(1) = 1
F(N) = F(N - 1) + F(N - 2), 其中 N > 1.
给定 N，计算 F(N)。

提示

0 ≤ N ≤ 30

示例
示例 1：
输入：2
输出：1
解释：F(2) = F(1) + F(0) = 1 + 0 = 1.

示例 2：
输入：3
输出：2
解释：F(3) = F(2) + F(1) = 1 + 1 = 2.

示例 3：
输入：4
输出：3
解释：F(4) = F(3) + F(2) = 2 + 1 = 3.
'''

'''
# Python特有， 常规写法
def fib(n):
    a = 0
    b = 1
    while a <= n:
        print(a, end=" ", flush=True)
        a, b = b, a + b  # python不借助变量交换两数的值


fib(100)  # 求n之内的斐波那契数列
'''


# 递归
def fibonacci(i):
    num_list = [0, 1]
    if i < 2:
        return num_list[i]
    elif i >= 2:
        return (fibonacci(i - 2) + fibonacci(i - 1))


print(fibonacci(10))


# 递归简写
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)


# 生成器
def fib_loop_while(max):
    a, b = 0, 1
    while max > 0:
        a, b = b, a + b
        max -= 1
        yield a


for i in fib_loop_while(10):
    print(i)


# 公式
def fib(N):
    return int((5 ** 0.5) * 0.2 * (((1 + 5 ** 0.5) / 2) ** N - ((1 - 5 ** 0.5) / 2) ** N))
