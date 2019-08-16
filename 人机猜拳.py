import random  #导入随机模块

print("-"*15,"欢迎进入游戏世界","-"*15)#字符串拼接
print("""
                *******************
                **   猜拳，开始  **
                *******************     \n""")
print("出拳规则：1.剪刀 2.石头 3.布")
ai1 = int(input("请选择对方角色（1：刘备 2：孙权 3：曹操）："))
me1 = input("请输入你的姓名：")
if ai1 == 1:
    ai1 = "刘备"
elif ai1 ==2:
    ai1 = "孙权"
else:
    ai1 = "曹操"
print("{}   VS   {}  对战\n".format(me1,ai1))

p = input("要开始吗？(y/n)")
print()     #空一行

if  p == "y":  #输入不是N
    # 猜拳判断
    def ran():
        ai_ran1 = random.randint(1, 3)
        if ai_ran1 == 1:  # 电脑出拳的判断
            a1 = "剪刀"
        elif ai_ran1 == 2:
            a1 = "石头"
        elif ai_ran1 == 3:
            a1 = "布"

        l = int(input("请出拳：1.剪刀 2.石头 3.布（输入相应数字）:"))
        if l == 1:  # 你出拳的判断
            l1 = "剪刀"
        elif l == 2:
            l1 = "石头"
        elif l == 3:
            l1 = "布"

        if l == 1 and ai_ran1 == 3 or l == 2 and ai_ran1 == 1 or l == 3 and ai_ran1 == 1:
            print("你出拳：{}\n{}出拳：{}\n结果：恭喜，你赢了！\n".format(l1, ai1, a1))
            return l2
        elif l == 1 and ai_ran1 == 2 or l == 2 and ai_ran1 == 3 or l == 3 and ai_ran1 == 1:
            print("你出拳：{}\n{}出拳：{}\n结果：^_^，你输了，真笨！\n".format(l1, ai1, a1))
            return ai2
        else:
            print("你出拳：{}\n{}出拳：{}\n结果：和局，真衰！嘿嘿，等着瞧吧！\n".format(l1, ai1, a1))
            return 0


    l2 = 0  # 你赢多少
    ai2 = 0  # 电脑赢多少局

    sun = 0  # 多少局
    while True:
        j = ran()  # 调用
        if j == l2:  # 你赢+1
            l2 += 1
        elif j == ai2:  # 电脑赢+1
            ai2 += 1
        sun += 1  # 回合+1

        p1 = input("是否开始下一轮（y/n）：")
        print()     #空一行

        if p1 == "y":
            pass
        else:
            print("-" * 30)
            print("{}   VS   {}  对战\n对战次数：{}".format(me1, ai1, sun))
            print("姓名     得分")
            print("{}     {}\n{}     {}".format(me1, l2, ai1, ai2))
            break
            # 结束游戏
else:
    print("游戏结束")
