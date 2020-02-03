import random


class RedPacket:
    def __init__(self, money):
        self.money = money

    def similar_packet(self, n, floats=(0.2,0.5)):
        '''
        :param n: 红包个数
        :param floats: 单个平均额度浮动值（最低百分比，最高百分比）
        :return:
        '''
        print('随机抢红包······')
        hongbao_list = [self.shuiji(n,floats) for x in range(n-1)]
        while sum(hongbao_list) >= self.money:
            hongbao_list = [self.shuiji(n,floats) for x in range(n-1)]
        hongbao_list.insert(int(random.randint(0,n)),self.money - sum(hongbao_list))

        count = 1
        print('实际金额',sum(hongbao_list))
        while count <= n:
            if count < n:
                print("第[%s]个人抢红包金额是%0.2f元" % (count, hongbao_list.pop()))
            else:
                print("第[%s]个人抢红包金额是%0.2f元" % (count, hongbao_list.pop()))
            count += 1


    def shuiji(self,n,floats):
        return round((self.money / (n + random.randint(-round(n*floats[0]), round(n*floats[1])))) + round(random.random(), 2), 2)

rp = RedPacket(float(input('总金额：')))
rp.similar_packet(int(input('红包个数：')))


