import sys
import threading
from re import sub
from os import system
from time import sleep, time

# 全局参数
amount_sum = 100  # 总的数量
current_number = 0  # 现在的数量

# 前五个位置固定的
text = '''
***************************************************************
{0}/{1} 进度:{2}%   已用时:{3}   剩余时间:{4}

'''


class MultiLineRefresh(threading.Thread):

    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.__flag = threading.Event()  # 用于暂停线程的标识
        self.__flag.set()  # 设置为True
        self.__running = threading.Event()  # 用于停止线程的标识
        self.__running.set()  # 将running设置为True
        self.start_time = time()

    # 主体部分
    def run(self):
        global text, amount_sum, current_number  # 全局的文本

        while self.__running.isSet():
            current_number += 1
            if amount_sum != 0 and current_number != 0:
                sleep(0.25)
                self.__flag.wait()  # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回
                ues_time, res_time = self.time_change(current_number, amount_sum, self.start_time)
                a = text.format(current_number, amount_sum,
                                round(current_number / amount_sum * 100, 2), ues_time, res_time)
                system('cls')  # 清空终端
                a = sub('', '', a)  # 修改文本
                sys.stdout.write("\r{}".format(a))  # 显示
                sys.stdout.flush()  # 刷新缓冲区
            if current_number == amount_sum:
                print('运行结束...')
                self.stop()

    # 暂停
    def pause(self):
        self.__flag.clear()  # 设置为False, 让线程阻塞

    # 恢复
    def resume(self):
        self.__flag.set()  # 设置为True, 让线程停止阻塞

    # 停止
    def stop(self):
        self.__flag.set()  # 将线程从暂停状态恢复, 如何已经暂停的话
        self.__running.clear()  # 设置为False

    # 秒数转时间格式
    def datetimes(self, s):
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)
        return "%d:%02d:%02d" % (h, m, s)

    # 现在的数量，总的数量，开始的时间
    def time_change(self, current_number, amount_sum, start_time):
        present_time = time()
        elapsed_time = float(present_time - start_time)
        average_time = elapsed_time / current_number
        scheduled_time = (amount_sum - current_number) * average_time
        return self.datetimes(elapsed_time), self.datetimes(scheduled_time)


MultiLineRefresh().start()
