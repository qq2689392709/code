
import random


class Name():
    def __init__(self,name,status):
        self.name = name
        self.status = status
        self.card = []
        self.score = 0
        self.explode = False

    # 输出格式化
    def __str__(self):
        return f"名字:{self.name.ljust(5)}\t身份:{'庄家' if self.status else '闲家'}\t点数:{self.score}\t\t爆点:{'是' if self.explode else '否'}\t手牌:{self.card}"


class Card():

    def __init__(self,library,objs):
        # 玩家对象
        self.objs = objs
        # 牌库
        self.library = library
        # 洗牌
        self.presuffling()

    # 洗牌
    def presuffling(self):
        return random.shuffle(self.library)

    # 抽牌
    def deal(self):
        self.objs.card.append(self.library.pop())

    # 计算点数
    def count(self):
        self.objs.score = sum([self.co(x) for x in self.objs.card])

    # 特殊牌 'A','J','Q','K'
    def co(self,c):
        if c in ['J', 'Q', 'K']:
            return 10
        elif c == 'A':
            return 11
        else:
            return int(c)

    # 爆点
    def explode(self):
        count_A = self.objs.card.count('A')
        if self.objs.score > 21 and count_A == 0:
            self.objs.explode = True
        elif self.objs.score > 21 and count_A:
            self.objs.score = self.objs.score - (count_A * 10)

    # 要牌
    def wantCard(self):
        # 要牌概率
        def ToF():
            if len([x for x in self.library if self.objs.score + self.co(x) < 21]) / len(self.library) > 0.4:
                return True

        if self.objs.explode == False:
            if self.objs.status == 1:
                # 庄家不得低于16点
                while self.objs.score < 16:
                    self.deal()
                    self.count()
                    # 大于16点后看概率抽卡
                    if self.objs.score > 16 and not ToF():
                        break
                self.explode()

            elif self.objs.status == 0:
                # 闲家不得超过21点，概率抽卡
                while self.objs.score < 21 and ToF():
                    self.deal()
                    self.count()
                self.explode()


# num = int(input('有几位玩家？：'))
# name = input('您叫什么？')
# status = int(input('您是庄家还是闲家？1或0:'))
num = 10
name = '2B'
status = 0
# 牌库，除大小鬼四副
library = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'] * 4 * 4
C = "Card(library,Name('{}',int({})))"

# 创建玩家对象列表
if status:
    nums_list = [eval(C.format(f'闲家{x+1}',0)) for x in range(num-1)] + [eval(C.format(name,1))]
else:
    rnum = random.randint(0, num - 2)
    nums_list = [eval(C.format(name,0)) if x == rnum else eval(C.format(f'闲家{x+1}',0)) for x in range(num - 1) ] + [eval(C.format('庄家',1))]

# 遍历，然后掉用要牌
for i in nums_list:
    i.wantCard()
    print(i.objs)
