# 超压缩3行，一行导包、一行定义参数、一行主体 239个字符
import random
rand, i, n = random.randint(1, 100), 1, 5
while i <= n:num = int(input('猜猜多少?(1-100):'));print(f'{exec("""print("猜对了，游戏结束");exit()""")}' if rand == num else '不对，大了' if num > rand else '不对，小了');i += -(n-1) if i == n and (True if input('是否继续？y/n:') == 'y' else print('游戏结束')) else 1


# 数字范围100，猜5次询问是否继续。
import random

rand, i, n = random.randint(1, 100), 1, 5
'''
rand：范围
i：初始次数
n：猜几次
'''
while i <= n:
    num = int(input('猜猜多少?(1-100):'))
    print(f'{exec("""print("猜对了，游戏结束");exit()""")}' if rand == num else '不对，大了' if num > rand else '不对，小了')
    # 修改次数的值，当次数和猜几次相符，询问是否继续，如果继续次数就初始回1，不继续则打印结束
    i += -(n-1) if i == n and (True if input('是否继续？y/n:') == 'y' else print('游戏结束')) else 1
