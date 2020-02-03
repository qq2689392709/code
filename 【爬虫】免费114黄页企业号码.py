import csv
import os
import threading
import requests
import lxml
from lxml import etree
from re import sub, search
from math import floor

# 这个需要安装 pip install ngender
import ngender
from fake_useragent import UserAgent


num = 0
gnum = 0
name = ''
nlist = []




# 模拟浏览器的请求头
def get_header():
    return {
        'User-Agent': UserAgent().firefox,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
    }


# 获取页面
def get_html(url, name=None):
    global nlist
    # 过滤掉之前也就获取的过的
    if name not in nlist:
        i = 0
        # 等待响应6秒，最多重连6次
        while i < 6:
            try:
                html = requests.get(url, headers=get_header(), timeout=6).content.decode('utf-8')
                return html
            except requests.exceptions.RequestException:
                i += 1
                print(f'重新连接{i}:{url}')

        with open('错误的url记录.txt', 'a', encoding='utf-8')as ur:
            ur.write(f'{url}\n')
            ur.close()
    else:
        nlist.remove(name)
        print(f'\r剩余跳过：{len(nlist)} {url} {name}',end='',flush=True)


# 获取地区目录
def get_url_name(req):
    '''
    :param req: str格式的html
    :return: [[url,name,地区],[url,name,地区]······]
    '''
    list1 = []
    html = lxml.etree.HTML(req)
    for i in html.xpath('//*[@id=\"subarealist\"]/div[2]/a'):
        list1.append(i.xpath('@href|text()'))
    return list1


# 获取行业目录
def get2_url_name(req):
    list1 = []
    html = lxml.etree.HTML(req)
    for i in html.xpath('//div[@class=\"tag_tx\"]//a'):
        list1.append(i.xpath('@href|text()'))
    return list1


# 获取页码，最少1最高50
def yema(req):
    if isinstance(req, str):
        html = lxml.etree.HTML(req)
        n = html.xpath('//span/em/text()')
        if n:
            if n[0].isdigit():
                n = int(n[0])
                return 50 if (n // 20) > 50 else (n // 20) + 1
        else:
            return 1
    return 1


# 获取企业目录内详细公司（网站最高只显示50页1千条）
def get3_url_name(urls, diqu):
    def emmm(url,req):
        global gnum
        if req and req.strip():
            ye = yema(req)
            for ye in range(1, ye + 1):
                list1 = []
                html = lxml.etree.HTML(get_html(f'{url}pn{ye}/'))
                for i in html.xpath('//*[@id=\"jubao\"]//h4/a'):
                    list1.append(i.xpath('@href|text()') + [diqu])
                    gnum += 1
                with open(f'{name}详细目录.txt', 'a', encoding='utf-8') as f:
                    f.write('\n'.join(map(str, list1)) + "\n")
                    f.close()
            print(f'\r以获取{gnum}个原始链接···', end='', flush=True)

    if isinstance(urls, list):
        emmm(urls[0],get_html(urls[0]))
    elif isinstance(urls, str):
        emmm(urls[0],get_html(urls))


# 获取名字和手机号
def get_name_cell_phone(req, x):
    '''
    :param req: str格式的html页面
    :param x: 目录列表，获取公司名和地区用的
    :param sex: 性别，male男性 female女性，基于朴素贝叶斯计算的概率推测
    :return: [[姓名,手机号,地区,公司名],[姓名,手机号,地区,公司名]······]
    '''
    if req.strip():
        html = lxml.etree.HTML(req)
        list1 = html.xpath('//ul[@class=\"con-txt\"]//label[contains(text(),"联系人：")]/following-sibling::a/text()')
        if not list1:
            list1 = html.xpath('//ul[@class=\"con-txt\"]//label[contains(text(),"联系人：")]/ancestor::li/text()')
        # TODO: xpath把这个特殊编码解析了无法转回来，只能正则匹配了
        # phone = html.xpath('//ul[@class=\"con-txt\"]//label[contains(text(),"手机：")]/following-sibling::span[1]/text()')
        if list1:
            try:
                # 过滤女性，非中文会报错
                unknown = ngender.guess(list1[0])
                # todo：返回格式('male', 0.9836229687547046)  预测的性别，男/女性化的深度
                if unknown[0] == 'male' or (unknown[0] == 'female' and unknown[1] < 0.7):
                    # 获取手机号原加密格式
                    phone = search("(?s)<span class='secret'>(.*?)</span>", req)
                    if phone:
                        # 解密，并添加地区和公司名
                        list2 = [int(sub('&#x', '0x', x), 16) for x in phone.group(1).split(';')[:-1]]
                        list1.extend([''.join([str(i - list2[0] + 1) for i in list2])+'\t', x[2], x[1]])
                        return list1
            except:
                # 获取手机号原加密格式
                phone = search("(?s)<span class='secret'>(.*?)</span>", req)
                if phone:
                    # 解密，并添加地区和公司名
                    list2 = [int(sub('&#x', '0x', x), 16) for x in phone.group(1).split(';')[:-1]]
                    list1.extend([''.join([str(i - list2[0] + 1) for i in list2])+'\t', x[2], x[1]])
                    return list1


# 保存csv
def save_csv(urllist):
    '''
    :param urllist: 这是线程入口，传入[[url,公司名,地区],[url,公司名,地区]······]
    :return:
    '''
    global num

    # 已访问过的公司保存名字，避免中断后重新获取
    with open(f'已访问过的{name}名单.txt', 'a', encoding='utf-8')as tf:

        for file_list in urllist:
            list1 = get_name_cell_phone(get_html(file_list[0] + 'company_contact.html', file_list[1]), file_list)
            if list1:
                num += 1
                with open(f'{name}.csv', 'a', encoding='utf-8', newline='') as cf:
                    csv_writer = csv.writer(cf)
                    csv_writer.writerow(list1)
                    cf.close()
                    print(f'{num} {list1} 写入完成')

            tf.write(f"{file_list[1]}\n")
        tf.close()


# 分隔列表,开线程用
def list_of_groups(init_list, list_len):
    l = len(init_list)
    list_len = floor(l * list_len) if floor(l * list_len) != 0 else 1
    list_of_group = zip(*(iter(init_list),) * list_len)
    end_list = [list(i) for i in list_of_group]
    count = len(init_list) % list_len
    end_list.append(init_list[-count:]) if count != 0 else end_list
    return end_list


# todo: 初始化开始的部分
def start(url):
    global nlist, name

    names = lambda: lxml.etree.HTML(get_html(url)).xpath('//div[@class=\"top_n\"]/h1/text()')[0]

    name = names()

    # 创建文件头
    if not os.path.isfile(f'{name}.csv'):
        f = open(f'{name}.csv', 'a', encoding='utf-8', newline='')
        csv_writer = csv.writer(f)
        csv_writer.writerow(['姓名', '手机号', '地区', '公司'])
        f.close()

    # 读取以保存过的公司名列表，重新抓取时跳过这些公司
    if os.path.isfile(f'已访问过的{name}名单.txt'):
        with open(f'已访问过的{name}名单.txt', 'r', encoding='utf-8')as yf:
            nlist = list(str(yf.readlines()))
            yf.close()

    # 从首页到一直获取到详细公司的url目录
    if not os.path.isfile(f'{name}详细目录.txt') or len(open(f'{name}详细目录.txt','r',encoding='utf-8').read()) < 10:
        for u in get_url_name(get_html(url)):
            print(f'正在获取：{u[1]}')
            hyml = get2_url_name(get_html(u[0]))
            t_list = []
            for i in list_of_groups(hyml, 0.1):
                t = threading.Thread(target=get3_url_name, args=(i[0], u[1].strip('企业名录')))
                t.start()
                t_list.append(t)
            for t in t_list:
                t.join()
    else:
        print(f'{name}详细目录.txt 文件已存在且不是空，跳过获取目录开始获取联系方式···')

    with open(f'{name}详细目录.txt', 'r', encoding='utf-8') as xf:
        xxml = [eval(x) for x in xf.readlines()]
        xf.close()

    t_list = []
    # 按行读取成列表后切割成小列表创建线程用 list_of_groups(原列表,百分比)
    # 把str格式的列表用eval()转回list格式
    for i in list_of_groups(xxml, 0.1):
        t = threading.Thread(target=save_csv, args=(i,))
        t.start()
        t_list.append(t)
    for t in t_list:
        t.join()

    print('代码运行完成。')


if __name__ == '__main__':
    # try:
    print('开始获取')
    html = lxml.etree.HTML(get_html('http://b2b.huangye88.com/region/'))
    city_dict = {}
    for i in html.xpath('//dl[@id=\"clist\"]//dd/a'):
        value, key = i.xpath('@href|text()')
        city_dict[key] = value
    print('不建议连续爬取多个城市，会被屏蔽')
    print(city_dict.keys())
    name = input('请输入城市名：').strip('市')
    # name = '南京'
    url = city_dict.get(name)
    if url:
        # todo：开始部分，输入url
        start(url)
    else:
        print('城市名搜索失败，请确认网址是否支持该城市···')

    # except BaseException as error:
    #     print(f'错误类型:{error.__class__}\n错误原因:{error}\n错误行数:{error.__traceback__.tb_lineno}\n自己改代码出BUG自己解决.笑')
