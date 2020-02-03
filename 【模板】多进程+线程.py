import time
import requests
import re
import multiprocessing
import threading

# 模拟浏览器
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36"
}


# 获取所有区
def get_all_area():
    url = 'https://sz.lianjia.com/ershoufang/pg1/'
    response = requests.get(url, headers=headers)
    content = response.text

    pattern = '<div data-role="ershoufang" >(.*?)</div>'
    area_str = re.findall(pattern, content, re.S)[0]
    # print(area_str)

    url_pattern = 'href="(.*?)"'
    url_list = re.findall(url_pattern, area_str, re.S)
    # print(url_list)

    areaname_pattern = '<a(?:.*?)>(.*?)</a>'
    areaname_list = re.findall(areaname_pattern, area_str, re.S)
    # print(areaname_list)

    return url_list, areaname_list


# 获取当前区下的每一页数据
def get_page(page, url, area):
    url = '%s/pg%d/' % (url, page)
    response = requests.get(url, headers=headers)
    # print('第%d页' % page, len(response.text))
    print('{}:第{}页'.format(area, page))


# 获取每个区下的所有分页数据
def get_area(url, area):
    # 使用协程
    t_list = []
    for i in range(1, 101):
        t = threading.Thread(target=get_page, args=(i, url, area))
        t.start()
        t_list.append(t)

    for t in t_list:
        t.join()


if __name__ == '__main__':
    # 获取所有区
    url_list, area_list = get_all_area()

    s = time.time()
    p_list = []
    for i in range(len(url_list)):
        url = 'https://sz.lianjia.com' + url_list[i]
        area = area_list[i]

        p = multiprocessing.Process(target=get_area, args=(url, area))
        p.start()
        p_list.append(p)

    for p in p_list:
        p.join()

    e = time.time()
    print(e - s)
