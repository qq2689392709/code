import csv
import threading
import requests
import lxml
from lxml import etree
from random import choice
import re


USER_AGENTS = [
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

def get_header():
    return {
        'User-Agent': choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
    }


def get_html(url):
    i = 0
    url = re.sub('review/','',url)
    while True:
        try:
            html = requests.get(url, headers=get_header(), timeout=6).content.decode('utf-8')
            return html
        except requests.exceptions.RequestException:
            i += 1
            print(f'重新连接{i}:{url}')
        except:
            print('未知异常')


def get_url_name(req):
    list1 = []
    html = lxml.etree.HTML(req)
    for i in html.xpath('//*[@id="content_3col"]/table//*[@width=\"33%\"]//a'):
        list1.append(i.xpath('@href|text()'))
    return list1


def get_table(req):
    list1 = []
    html = lxml.etree.HTML(req)
    for i in html.xpath('//table[@class="form"][1]//tr'):
        list1.append(i.xpath('th/text()|td[2]/b/text()|td[2]/text()|td[2]/a/text()'))

    guo = html.xpath('//*[@class=\"breadcrumb_off\"]')
    if guo:
        guo = guo[0]
        continent, state, name = guo.xpath('string()').split(' >> ')[2:5]
        if list1:
            list1[0] = ['State', state]
            list1.insert(0, ['Continent', continent])
        else:
            list1 = [['Continent', continent], ['State', state], ['Port Location', name]]

    return list1


num = 0


def duo(urllist):
    global num
    for file_list in urllist:
        num += 1
        list1 = get_table(get_html(file_list[2]))[:-1]
        csv_writer.writerow(['' if not x[1:] else x[1] for x in list1])
        print(f'{num} {file_list[0]}:{file_list[1]} 写入完成')


if __name__ == '__main__':
    print('开始获取')
    # url = 'http://www.worldportsource.com/countries.php'
    # # 获取页面
    # req = get_html(url)
    # print('首页获取成功')
    # # 获取首页页面的url和名字
    # list1 = get_url_name(req)
    # print('目录获取成功')
    # for url1,name1 in list1:
    #     nwe_url = 'http://www.worldportsource.com' + url1
    #     for url2, name2 in get_url_name(get_html(nwe_url)):
    #             nwe_url2 = 'http://www.worldportsource.com' + url2
    #             with open('port.txt','a',encoding='utf-8') as f:
    #                 f.write(f'["{name1}","{name2}","{nwe_url2}"]\n'.encode().decode('utf-8'))
    #                 print(f'{name1}:{name2}')
    # print('详细目录获取完成')

    try:
        f = open('port.csv', 'a', encoding='utf-8', newline='')
        csv_writer = csv.writer(f)
        csv_writer.writerow(
            ['Continent', 'State', 'Port Location', 'Port Name', 'Port Authority', 'Address', 'Phone', 'Fax',
             '800 Number:', 'Email', 'Web Site', 'Latitude', 'Longitude', 'UN/LOCODE', 'Port Type', 'Port Size'])
        with open('port.txt', 'r', encoding='utf-8') as f:
            file = f.readlines()
            url1 = [eval(x) for x in file[:500]]
            url2 = [eval(x) for x in file[500:1000]]
            url3 = [eval(x) for x in file[1000:1500]]
            url4 = [eval(x) for x in file[1500:2000]]
            url5 = [eval(x) for x in file[2000:2500]]
            url6 = [eval(x) for x in file[2500:3000]]
            url7 = [eval(x) for x in file[3000:3500]]
            url8 = [eval(x) for x in file[3500:4000]]
            url9 = [eval(x) for x in file[4000:4500]]
            url10 = [eval(x) for x in file[4500:5000]]
            url11 = [eval(x) for x in file[5000:]]
            t_list = []
            for i in [url1, url2, url3, url4, url5, url6, url7, url8, url9, url10, url11]:
                t = threading.Thread(target=duo, args=(i,))
                t.start()
                t_list.append(t)
            for t in t_list:
                t.join()
            f.close()
            print('完成')

    except:
        f.close()
        print('异常')

    # 读取排序
    with open('port.csv', 'r', encoding='utf-8') as csvFile:
        reader = csv.reader(csvFile)
        list1 = list(reader)
        list2 = sorted(list1[1:], key=lambda x: x[1])
    # 重新写入保存
    with open('port2.csv', 'w', encoding='utf-8', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(
            ['Continent', 'State', 'Port Location', 'Port Name', 'Port Authority', 'Address', 'Phone', 'Fax',
             '800 Number:',
             'Email', 'Web Site', 'Latitude', 'Longitude', 'UN/LOCODE', 'Port Type', 'Port Size'])
        writer.writerows(list2)
