import random


def win_or_lose(ai, user):
    return '平' if ai == user else '赢' if ai == (user + 1) % 3 else '输'

def main():
    mora = ['石头', '剪刀', '布']
    ai = random.randint(1, 3)
    user = input('请输入你要的拳：')

    # 验证输入是否有效
    if user in mora + ['1', '2', '3']:
        user = int(user) if user.isdigit() else mora.index(user) + 1
        # result = win_or_lose(ai, user)
        # win_or_lose = lambda ai, user:'平' if ai == user else '赢' if ai == (user + 1) % 3 else '输'
        result = win_or_lose(ai, user)

        # 打印结果
        print(f'你{result}了' if result != '平' else '平局', f'电脑出的拳是：{mora[ai - 1]}\n')

    else:
        print('你输入有误哦~\n')


if __name__ == '__main__':
    print("猜拳小游戏规则：\n  请输入'石头'、'剪刀'、'布'或者'1'、'2'、'3'来选择您要出的拳。\n")

    while True:
        main()
