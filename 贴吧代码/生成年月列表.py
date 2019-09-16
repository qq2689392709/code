'''
题目

从现在的月份往前推25个月，格式2019年09月，放在一个列表里。
'''

# time 版本
import time

tm = lambda x: time.localtime(time.time() - 2649600.0 * x)
print([f'{tm(x).tm_year}年{tm(x).tm_mon}月' for x in range(25)])

# datetime 版本
from datetime import datetime

y, m, *_ = datetime.now().timetuple()
print([f'{y + ((m - i) // 12)}年{(m - i + 1) % 12 if (m - i + 1) % 12 else 12}月' for i in range(1,26)])
