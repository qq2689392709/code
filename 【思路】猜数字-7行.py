
# 自定义范围和次数
# 主体用了三目运算和exec()方法
import random

mi, ma, n = map(int, input('最小值 最大值 次数(空格分隔)：').split())
rand, numb= random.randint(mi, ma), 1
while numb <= n:
    num = int(input(f'还有{n - numb}次机会，猜猜多少?({mi}~{ma}):'))
    # 11行和12行是一行代码
    print((f'''{exec('print("猜对了，游戏结束");exit()')}''' if rand == num else f"不对，大了{exec('ma=num')}"
    if num > rand else f"不对，小了{exec('mi=num')}").strip('None'))
    numb += -(n - 1) if numb == n and (True if input('是否继续？y/n:') == 'y' else print('游戏结束')) else 1
