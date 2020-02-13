

import requests
import lxml
from lxml import etree
from fake_useragent import UserAgent
from time import sleep
import threading

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

    def xici():
        try:
            # 一页100
            for i in range(1, 3):
                url = f'http://www.xicidaili.com/nn/{i}'
                req = requests.get(url, headers=get_header()).content.decode('utf-8')
                ip_list = lxml.etree.HTML(req).xpath('//tr')
                for x in ip_list[1:]:
                    ip = ":".join(x.xpath('td[2]/text()|td[3]/text()'))
                    http = x.xpath('td[6]/text()')[0]
                    proxy.append([http.lower(),ip])
        except:
            pass


    def kuai():
        try:
            # 一页15
            for i in range(1,11):
                url = f'https://www.kuaidaili.com/free/inha/{i}/'
                req = requests.get(url, headers=get_header()).content.decode('utf-8')
                ip_list = lxml.etree.HTML(req).xpath('//div[@id=\"list\"]/table/tbody/tr')
                for x in ip_list:
                    ip = ":".join(x.xpath('td[1]/text()|td[2]/text()'))
                    http = x.xpath('td[4]/text()')[0]
                    proxy.append([http.lower(), ip])
                sleep(1)
        except:
            pass

    x = threading.Thread(target=xici,args=())
    x.start()
    k = threading.Thread(target=kuai,args=())
    k.start()
    for t in [x,k]:
        t.join()
    return proxy

def validate_ip(ip_list):
    index = 0
    agency = []
    url = "http://www.httpbin.org/ip"

    def get_ip(proxys):
        for ips in proxys:
            http, ip = ips
            try:
                proxy = {'http': f'{http}://{ip}'}
                # 响应时间可以设置1秒，只要高效ip
                req = requests.get(url=url,headers=get_header(),proxies=proxy,timeout=1).json()
                if req["origin"] == ip.split(':')[0]:
                    agency.append(proxy)
                    print(f'成功：{ip} {req["origin"]}')
                else:
                    print(f'失败：{ip} {req["origin"]}')

            except Exception as e:
                print(f'{http}://{ip} 请求异常和连接超时')
        return agency

    x = threading.Thread(target=get_ip, args=(ip_list[:len(ip_list)//2],))
    x.start()
    k = threading.Thread(target=get_ip, args=(ip_list[len(ip_list)//2:],))
    k.start()
    for t in [x, k]:
        t.join()
    return agency

ip = get_proxyIp()
print(ip)
print(validate_ip(ip))
