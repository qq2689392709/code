import os
import re

def findtxt(path, ret):
    try:
        filelist = os.listdir(path)
        for filename in filelist:
            de_path = os.path.join(path, filename)
            if os.path.isfile(de_path):
                if de_path.endswith(".py"):  # Specify to find the txt file.
                    ret.append(de_path)
            else:
                findtxt(de_path, ret)
    except:
        pass


ret = []
# 项目绝对地址地址
root = r"D:\git\tinatian"
findtxt(root, ret)

konbai = 0
daima = 0
zhushi = 0
for path in ret:
    with open(path,'r',encoding='utf-8')as f:
        for j in f.readlines():
            nei = "".join(j.strip())
            if re.match('#',nei):
                zhushi += 1
            elif nei == '':
                konbai += 1
            else:
                daima += 1

print('后端部分python代码统计：\n\n空白行:{}  注释行:{}  代码行:{}  注释比例:{:.2f}%'.format(konbai,zhushi,daima,(zhushi/(zhushi+daima))*100))




# 获取指定后缀文件
import os
import re

# 1.遍历全部文件夹
def get_files(dir,suffix):
    res = []

    for root,dirs,files in os.walk(dir):
        for filename in files:
            name,suf = os.path.splitext(filename)
            if suf == suffix:
                res.append(os.path.join(root,filename))

    print(res)

# 2.只获取当前文件夹
def get_file(dir,suffix):
    res = []

    for file in os.listdir(dir):
        if re.match(r'.*\.%s'%suffix,file):
            res.append(file)

    print(res)


# 3.一行获取当前文件夹指定文件后缀
print([file for file in os.listdir('./') if re.match(r'.*\.py', file)])




## 输入某年某月某日，判断这一天是这一年的第几天？
# import datetime
#
# y = int(input("请输入4位数字的年份:"))
# m = int(input("请输入月份:"))
# d = int(input("请输入是哪一天"))
#
# targetDay = datetime.date(y,m,d)
# dayCount = targetDay - datetime.date(targetDay.year -1,12,31)
#
# print("%s是 %s年的第%s天。"%(targetDay,y,dayCount.days))


## 获取指定大小列表
# print ([[x for x in range(i,i+3 if i+3<100 else 100)] for i in range(1,100,3)])



