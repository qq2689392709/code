import time
import requests

def youdao(kw):
    url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule"
    header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36"
        }
    timet = int(time.time() * 1000)
    data = {
        "i": kw,
        "from": "AUTO",
        "to": "AUTO",
        "smartresult": "dict",
        "client": "fanyideskweb",
        "salt": timet,
        "sign": "f66461b42fe9edb6d88230788fb33cfb",
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "action	": "FY_BY_REALTIME",
        "typoResult	": "false",
    }
    response = requests.post(url, data=data, headers=header)
    res = response.json()
    print(f'翻译:{res["translateResult"][0][0]["tgt"]}')

if __name__ == '__main__':

    kw = input("内容:")
    youdao(kw)
