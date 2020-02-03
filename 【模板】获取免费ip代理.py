# encoding=utf8
import requests
import lxml
from lxml import etree
from fake_useragent import UserAgent



# 模拟浏览器的请求头
def get_header():
    return {
        'User-Agent': UserAgent().firefox,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
    }

'''
获取所有代理IP地址
'''


def get_proxyIp():
    proxy = []

    try:
        # 一页100
        for i in range(1, 2):
            url = f'http://www.xicidaili.com/nn/{i}'
            req = requests.get(url, headers=get_header()).content.decode('utf-8')
            ip_list = lxml.etree.HTML(req).xpath('//tr')
            for x in ip_list[1:]:
                ip = ":".join(x.xpath('td[2]/text()|td[3]/text()'))
                http = x.xpath('td[6]/text()')[0]
                proxy.append([http.lower(),ip])
        # 一页15
        for i in range(1,3):
            url = f'https://www.kuaidaili.com/free/inha/{i}/'
            req = requests.get(url, headers=get_header()).content.decode('utf-8')
            ip_list = lxml.etree.HTML(req).xpath('//div[@id=\"list\"]/table/tbody/tr')
            for x in ip_list:
                ip = ":".join(x.xpath('td[1]/text()|td[2]/text()'))
                http = x.xpath('td[4]/text()')[0]
                proxy.append([http.lower(), ip])
    except:
        pass

    finally:
        return proxy


'''
验证获得的代理IP地址是否可用
'''

def validate_ip(proxys):
    agency = []
    url = "https://www.baidu.com/"
    f = open('D:\AAA\进阶\ip.txt','w',encoding='utf-8')
    for ips in proxys:
        http, ip = ips
        try:
            proxy = {'http': f'{http}://{ip}'}
            # 响应时间可以设置1秒，只要高效ip
            req = requests.get(url=url, headers=get_header(),proxies=proxy,timeout=1)
            if req.status_code == 200:
                agency.append(proxy)
                f.write(f'{ips}\n')

        except Exception as e:
            continue
    return agency


if __name__ == '__main__':
    print('获取中请等待。。。')
    ips = get_proxyIp()
    print(f'获取{len(ips)}个，验证中。。。')
    print(f"有效数量：{len(validate_ip(ips))}/{len(ips)}")
