import random
import re
from datetime import datetime

from django.http import HttpResponseRedirect
from django.urls import reverse




def is_session_login(func):
    def chek(request,*args,**kwargs):
        try:
            # 从session中取数据，如果取得到表示登录
            request.session['user_id']
            return func(request,*args,**kwargs)
        except:
            return HttpResponseRedirect(reverse('user:my_session_login'))
    return chek


# 随机ticket
def get_random_ticket():
    s='1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    ticket = ''
    for i in range(30):
        ticket += random.choice(s)
    return ticket

# 交易号
def get_trade_no():
    s='1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    trade = ''
    for i in range(30):
        trade += random.choice(s)
    return trade

# 获取订单号字符串
def get_order_sn():
    s = str(datetime.now())
    ss = re.sub('-|:| |\.','',s)
    ss = ss[:13]
    return ss


