import random as r
import time as t


class Person:
    # 实例化姓名
    def __init__(self, name):
        self.name = name
        # 体力默认100点
        self.life = 100

    def __str__(self):
        # 状态判断
        if self.life == 100:
            stat = "满血"
        elif 70 <= self.life < 100:
            stat = "轻伤"
        elif 20 <= self.life < 70:
            stat = "中伤"
        elif 1 <= self.life < 20:
            stat = "重伤"
        else:
            stat = "死亡"
        return "姓名: %s\t生命值: %d\t状态: %s" % (self.name, self.life, stat)


class Police(Person):
    # 开火
    def fire(self, i):
        if not i.name in surrender_member:
            # 只有生命值大于20的时候,警察才有能力开枪
            if self.life < 20:
                print("%s重伤状态,急需急救!" % self.name)
                print("%s是否需要急救" % self.name)
                chose = r.choice([-1, 0, 1])
                if chose > 0:
                    self.aid()
                else:
                    print("%s身负重伤仍不下火线,依然在第一线战斗着" % self.name)
            elif self.life == 0:
                print("%s在与恐怖分子战斗的过程中英勇牺牲了,%s是一个可歌可泣的人民英雄!" % (self.name, self.name))
            else:
                # 随机伤害
                damage = r.randint(10, 15)
                # 开枪命中率
                hit = r.randint(1, 100)
                if hit >= 20:
                    print("%s向%s开枪,%s击中了%s,造成了%d点伤害" % (self.name, i.name, self.name, i.name, damage))
                    # 防止生命值为负数
                    if i.life < damage:
                        i.life = 0
                    else:
                        i.life = i.life - damage
                else:
                    print("%s向%s开枪,%s并未击中了%s" % (self.name, i.name, self.name, i.name))
        else:
            print("%s已经投降了,不能伤害俘虏" % i.name)

    def aid(self):
        chose = r.choice([-3, -2, -1, 0, 1])
        if chose > 0:
            self.life += 30
            print("%s经过急救,伤情得到控制!继续参加战斗" % self.name)
        else:
            self.life += 20
            print("%s经过急救,伤情得到控制!继续参加战斗" % self.name)


surrender_member = []


class Is(Person):
    def fire(self, p):
        if not self.name in surrender_member:
            # 只有生命值大于20的时候,恐怖分子才有能力开枪
            if 1 < self.life <= 20:
                self.surrender(p)
            elif self.life == 0:
                print("%s负隅抵抗,不肯投降,被%s击毙了!" % (self.name, self.name))
            else:
                # 随机伤害
                damage = r.randint(10, 15)
                # 开枪命中率
                hit = r.randint(1, 100)
                if hit >= 70:
                    print("%s向%s开枪,%s击中了%s,造成了%d点伤害" % (self.name, p.name, self.name, p.name, damage))
                    # 防止生命值为负数
                    if p.life <= damage:
                        p.life = 0
                    else:
                        p.life = p.life - damage
                else:
                    print("%s向%s开枪,%s并未击中了%s" % (self.name, p.name, self.name, p.name))
        else:
            print("%s已经被警察逮捕了,无法开枪射击!" % self.name)

    def surrender(self, p):
        if self.name not in surrender_member:
            print("%s重伤,%s给了%s3秒的时间考虑是否投降" % (self.name, p.name, self.name))
            t.sleep(0.1)
            print("%s是否向%s投降" % (self.name, p.name))
            chose = r.choice([-2, -1, 0, 1])
            if chose <= 0:
                print("%s拒绝向%s投降, 决定一条路走到黑!" % (self.name, p.name))
                self.aid()
            else:
                print("%s向%s投降!,此时%s的生命值还有%d" % (self.name, p.name, self.name, self.life))
                surrender_member.append(self.name)
                return

    def aid(self):
        chose = r.choice([-1, 1])
        if chose >= 0:
            self.life += 15
            print("%s自行急救,伤情得到控制!继续攻击警察" % self.name)
        else:
            self.life += 10
            print("%s自行急救,伤情得到控制!继续攻击警察" % self.name)


def run():
    police = []
    p1 = Police("警察1号")
    p2 = Police("警察2号")
    police.append(p1)
    police.append(p2)
    iss = []
    is1 = Is("劫匪1号")
    is2 = Is("劫匪2号")
    is3 = Is("劫匪3号")
    iss.append(is1)
    iss.append(is2)
    iss.append(is3)
    count = 1
    iss1 = []
    iss2 = []
    police2 = []
    while True:
        print("【第{}个回合】\n".format(count))

        for c in police:
            if not c.life == 0:
                for a in iss[:]:
                    if not a.life == 0:
                        iss1.append(a)
                chose = r.choice(iss1)
                c.fire(chose)
            else:
                print("%s已经牺牲,无法开枪射击!" % c.name)
        for s in iss:
            if not s.life == 0:
                for e in police[:]:
                    if not e.life == 0:
                        police2.append(e)
                z = r.choice(police2)
                s.fire(z)
            else:
                if s.name not in iss2:
                    iss2.append(s.name)
                print("%s已经被警察击毙,无法开枪射击" % s.name)

        print()
        # 警察信息
        for p in police:
            print(p)

        # 劫匪信息
        for i in iss:
            print(i)

        count += 1

        if p1.life == 0 and p2.life == 0:
            print("警察全部牺牲,恐怖分子逃跑了!")
            break
        if len(iss2) == len(iss):
            print("{} 全部被击毙,警察胜利!".format("、".join(iss2)))
            break
        if len(surrender_member) == len(iss):
            print("{} 全部被捕,警察胜利!".format("、".join(surrender_member)))
            break
        if len(surrender_member)+len(iss2) == len(iss):
            print("{}被捕, {}被击毙,警察胜利".format('、'.join(surrender_member),'、'.join(iss2)))
            break

        print('\n','*'*50,'\n')
        t.sleep(0.2)
run()
