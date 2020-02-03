import re

import requests


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}

#解析网页
def parse_html(url):
    res = requests.get(url, headers=headers, verify=False)
    #返回正常
    if res.status_code == 200:
        html = res.text
    else:
        html = ''

    return html

#取出子url
def get_son_url(html):
    #子url的正则
    url_re = '<a.*?href="(.*?)".*?</a>'
    url_list = re.findall(url_re,html)
    #返回子url的列表
    return url_list

#爬取
def deep_spider(url,deep_level):

    url_list=[]
    url_list.append(url)

    #当url_list有内容时一直爬
    while len(url_list):

        #取出一个url
        url = url_list.pop()
        #对比当前层级，如果层级大于要爬层级，就返回
        if url_dict[url] > deep_level:
            continue

        #打印层级信息，和当前的url
        print('\t'*url_dict[url],f'当前的层级为：{url_dict[url]} url:{url}')

        html = parse_html(url)
        #如果是空，中断当前的爬取
        if not html:
            continue

        try:
            #子url的列表
            son_url_list = get_son_url(html)

        #如果出现错误，就跳过
        except Exception as e:
            continue

        #循环每一个url
        for son_url in son_url_list:
            if son_url.startswith('http'):

                #判断是否在url字典中,如果没有在，就去爬，如果已经存在，说明已经爬过
                if (son_url in url_dict) or son_url.endswith('exe'):
                    continue
                # 保存son_url到字典中，value为当前层级 + 1
                url_dict[son_url] = url_dict[url] + 1

                #把当前页面中的url回到列表当中
                url_list.append(son_url)


if __name__ == '__main__':
    #创建一个字典保存爬过的url
    url_dict = {}
    url = 'https://www.meijutt.com/'
    url_dict[url] = 1

    #爬取三层
    deep_spider(url,3)
