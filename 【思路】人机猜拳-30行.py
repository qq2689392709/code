import random


def main():
    mora = ['石头', '剪刀', '布']
    ai = random.randint(1, 3)
    user = input('请输入你要的拳：')

    # 验证输入是否有效
    if user in mora + ['1', '2', '3']:
        user = int(user) if user.isdigit() else mora.index(user) + 1

        # 判断输赢
        win_or_lose = lambda ai, user: '平局' if ai == user else '你赢了' if ai == (user + 1) % 3 else '你输了'
        result = win_or_lose(ai, user)

        # 打印结果
        print(f'{mora[user - 1]} VS {mora[ai - 1]}\n{result}\n')

    else:
        print('你输入有误哦~\n')

print("猜拳小游戏规则：\n  请输入'石头'、'剪刀'、'布'或者'1'、'2'、'3'来选择您要出的拳。\n")

while True:
    main()
