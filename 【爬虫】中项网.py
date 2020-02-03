import os
import sys

import requests
import csv
import re
import random
import time
import threading
from lxml import etree


amount_sum = 0
current_number = 0
out = '''
***************************************************************
{0}/{1} 进度:{2}%   已用时:{3}   剩余时间:{4}

'''

def datetimes(s):
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return "%d:%02d:%02d" % (h, m, s)


def time_change(current_number, amount_sum, start_time):
    present_time = time.time()
    elapsed_time = float(present_time - start_time)
    average_time = elapsed_time / current_number
    scheduled_time = (amount_sum - current_number) * average_time
    return datetimes(elapsed_time), datetimes(scheduled_time)


def output():
    global amount_sum, current_number, out
    start = time.time()
    while True:
        time.sleep(0.1)
        if amount_sum != 0 and current_number != 0:
            os.system('cls')
            ues_time, res_time = time_change(current_number, amount_sum, start)
            a = out.format(current_number, amount_sum, round(current_number / amount_sum * 100, 2), ues_time, res_time)
            sys.stdout.write("\r{}".format(a))
            sys.stdout.flush()


out_thre = threading.Thread(target=output, args=())
out_thre.start()


class Money(threading.Thread):
    global amount_sum, current_number, out
    def __init__(self, threadname):
        threading.Thread.__init__(self, name=threadname)
        self.url = 'https://www.ccpc360.com/f/getProjectOnly.php'
        self.user_agent = [
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
            "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
            "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
            "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
            "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
            "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
            "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
            "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36"
        ]

    # 设置请求头
    def get_headers(self, url):
        headers = {
            'Accept ': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'PHPSESSID=q5n9r118kbm71bndf6jltgk4s2; 53gid2=10282459578013; 53gid0=10282459578013; 53gid1=10282459578013; 53revisit=1580617455892; 53kf_72212606_from_host=www.ccpc360.com; 53kf_72212606_keyword=https%3A%2F%2Fwww.ccpc360.com%2Fdo%2Flogin.php%3Faction%3Dquit; 53kf_72212606_land_page=https%253A%252F%252Fwww.ccpc360.com%252F; kf_72212606_land_page_ok=1; UM_distinctid=17004245a185ff-0c7ba448d641a6-b383f66-100200-17004245a197d5; 53uvid=1; onliner_zdfq72212606=0; Hm_lvt_f0c9f0bc5cfd139ffff12756d4ffa430=1580617458; invite_53kf_totalnum_1=2; CNZZDATA1277430626=496709097-1580615290-https%253A%252F%252Fwww.ccpc360.com%252F%7C1580620895; passport=57165%09stevenlu1972%09AFZXV1MKBlYMCAcAVVNQBFIGAlQKBVZbBQMFDABQVFM%3Dc6e2e2f6e5; visitor_type=old; USR=jofuxjzu%0970%091580623679%09http%3A%2F%2Fwww.ccpc360.com%2Fbencandy.php%3Ffid%3D146%26ccpc%3DVI70cXXDlVuN3hQQ62yxDjfF; Hm_lpvt_f0c9f0bc5cfd139ffff12756d4ffa430=1580623698',
            'Host': 'www.ccpc360.com',
            'Referer': url,
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': random.choice(self.user_agent)
        }
        return headers

    # 发送get请求,获取响应
    def parse_url(self, url):
        global amount_sum, current_number, out
        i = 1
        while i < 6:
            try:
                html = requests.get(url, headers=self.get_headers(url), timeout=5).text
                if self.getName() in out:
                    out = re.sub(f'{self.getName()}:.*?\n', f'{self.getName()}:{url}\n', out)
                else:
                    out += f'{self.getName()}:{url}\n'
                current_number += 1
                with open(f'{self.getName()}.txt', 'a') as f:
                    f.write(f'{url}\n')
                return html
            except requests.exceptions.RequestException:
                if self.getName() in out:
                    out = re.sub(f'{self.getName()}:.*?\n', f'{self.getName()}:{url}\n', out)
                else:
                    out += f'{self.getName()}:{url}\n'
                i += 1
            except Exception as e:
                print(f"{self.getName()}:get未知异常! {e}\n")
                break

        with open('错误的url记录.txt', 'a', encoding='utf-8')as ur:
            ur.write(f'{url}\n')
            ur.close()

    # 发送post请求,获取响应
    def post_url(self, data, url):
        global amount_sum, current_number, out
        i = 1
        while i < 6:
            try:
                html = requests.post(self.url, data=data, headers=self.get_headers(url), timeout=5).text
                return html
            except requests.exceptions.RequestException:
                out.format({self.getName(): url})
                i += 1
            except Exception as e:
                print(f"{self.getName()}:post未知异常! {e}\n")
                break

    #  正则表达式获取信息
    def get_info(self, html):
        text = etree.HTML(html)

        发行时间 = text.xpath('//b[contains(text(),"发行时间")]/../following-sibling::td[1]')
        发行时间 = 发行时间[0].xpath('string()') if 发行时间 else None

        所属领域类型 = text.xpath('//b[contains(text(),"所属领域类型")]/../following-sibling::td[1]')
        所属领域类型 = 所属领域类型[0].xpath('string()') if 所属领域类型 else None

        预算总投资额 = text.xpath('//b[contains(text(),"预算总投资额")]/../following-sibling::td[1]')
        预算总投资额 = 预算总投资额[0].xpath('string()') if 预算总投资额 else None

        投资性质 = text.xpath('//b[contains(text(),"投资性质")]/../following-sibling::td[1]')
        投资性质 = 投资性质[0].xpath('string()') if 投资性质 else None

        资金到位情况 = text.xpath('//b[contains(text(),"资金到位情况")]/../following-sibling::td[1]')
        资金到位情况 = 资金到位情况[0].xpath('string()') if 资金到位情况 else None

        项目建设等级 = text.xpath('//b[contains(text(),"项目建设等级")]/../following-sibling::td[1]')
        项目建设等级 = 项目建设等级[0].xpath('string()') if 项目建设等级 else None

        预计开建年月 = text.xpath('//b[contains(text(),"预计开建年月")]/../following-sibling::td[1]')
        预计开建年月 = 预计开建年月[0].xpath('string()') if 预计开建年月 else None

        预计截至日期 = text.xpath('//b[contains(text(),"预计截至日期")]/../following-sibling::td[1]')
        预计截至日期 = 预计截至日期[0].xpath('string()') if 预计截至日期 else None

        项目所在地 = text.xpath('//b[contains(text(),"项目所在地")]/../following-sibling::td[1]')
        项目所在地 = 项目所在地[0].xpath('string()') if 项目所在地 else None

        项目主要设备 = text.xpath('//h2[contains(text(),"项目主要设备")]/following-sibling::div[1]')
        项目主要设备 = re.sub(r'等\n*?（.*?）\n*?', '', 项目主要设备[0].xpath('string()'), re.S)

        lists = [发行时间, 所属领域类型, 预算总投资额, 投资性质, 资金到位情况, 项目建设等级, 预计开建年月, 预计截至日期, 项目所在地, 项目主要设备]
        pid = re.findall('var uname = (.*?);', html)
        data = {
            'pid': pid[0],
            'ptype': '1',
        }
        return (lists, data)

    # 写入csv文件
    def save_info(self, lists):
        with open('中项网数据2.csv', 'a', encoding='utf-8', newline='')as file:
            csv_writers = csv.writer(file)
            csv_writers.writerow(lists)

    # 主程序
    def run_project(self, url):
        # 发送get请求,获取响应
        html = self.parse_url(url)
        # 获取pid
        lists, data = self.get_info(html)
        # 发送post请求,获取主要信息
        message = self.post_url(data, url)
        if message:
            info = eval(message)
            lists.insert(0, re.sub('<font.*?font>', '', info['title']))
            lxr = (re.sub('<br.*?>', '\n', re.sub('<font.*?font>', '', info['yzdw'])).split('\n'))
            infomation = [lxr[0]]
            for r in lxr:
                if r.startswith('手机') or r.startswith('联系人'):
                    infomation.append(re.sub(r'\r', '', re.sub(r'\n', '', r)))
            lists.append(re.findall('\d、.*?。', info['content'])[0].strip('\n'))
            lists.append(re.findall('\d、.*?。', info['jzjt'])[0])
            lists.extend(infomation)
        return lists


def duo(index, urls):
    m = Money(f'线程{index + 1}')
    for i in urls:
        while True:
            try:
                lists = m.run_project(re.sub(r'\n', '', i))
                if lists:
                    m.save_info(lists)
                    break
                else:
                    print(lists)
            except Exception:
                break


def run():
    global amount_sum, current_number, out
    try:
        with open('url_num3.txt', 'r', encoding='utf-8', newline='')as f:
            lines = f.readlines()
            list1 = lines[:5000]
            list2 = lines[5000:10000]
            list3 = lines[10000:15000]
            list4 = lines[15000:20000]
            list5 = lines[20000:25000]
            list6 = lines[25000:]
            lists = [list1, list2, list3, list4, list5, list6]
            # lists = [list1]
            amount_sum = sum(map(len, lists))
            t_list = []
            for index, value in enumerate(lists):
                t = threading.Thread(target=duo, args=(index, value,))
                print(f'线程{index + 1}开始!')
                t.start()
                t_list.append(t)
            for t in t_list:
                t.join()
            f.close()
            print('完成')
            raise Exception('结束')

    except Exception as e:
        print(f'未知异常! {e}')


run()
