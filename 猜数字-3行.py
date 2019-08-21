# 超压缩3行，一行导包、一行定义参数、一行主体
# import random
# rand,i = random.randint(1,100),0
# while i <= 5:num = int(input('猜猜多少?(1-100):'));print(f'{exec("""print("猜对了，游戏结束");exit()""")}' if rand == num else '不对，大了' if num > rand else '不对，小了');i += -4 if i == 4 and input('是否继续？y/n:') == 'y' else 1

# 数字范围100，猜5次询问是否继续。
import random

rand, i = random.randint(1, 100), 0
while i <= 5:
    num = int(input('猜猜多少?(1-100):'))
    # 这里作弊用了exec
    print(f'{exec("""print("猜对了，游戏结束");exit()""")}' if rand == num else '不对，大了' if num > rand else '不对，小了')
    # 修改次数的值，如果继续就-4，不继续就会变5
    i += -4 if i == 4 and input('是否继续？y/n:') == 'y' else 1
