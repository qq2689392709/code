def main():
    print("=" * 32)
    print(" " * 5, "学生管理系统V1.0     ", "" * 8)
    print("1.创建文件夹", "" * 14)
    print("2.改变文件存储路径", "" * 14)
    print("3.读取学生名单", "" * 14)
    print("4.创建学生详细信息存储文本", "" * 14)
    print("5.增加学生详细信息", "" * 14)
    print("6.增加学生属性", "" * 14)
    print("7.查询所有学生信息", "" * 14)
    print("9.查询单个学生信息", "" * 14)
    print("10.修改学生信息", "" * 14)
    print("0.退出系统", "" * 14)
    print("=" * 32)
    while True:
        num = input("请输入要选择的功能:")
        if num == '1':
            wenjianjia()  # 创建文件夹
        elif num == "2":
            lujing()  # 改变文件存储路径
        elif num == "3":
            mingdan()  # 读取学生名单
        elif num == '4':
            wenben()  # 创建学生详细信息存储文本
        elif num == '5':
            xsxinxi()  # 增加学生详细信息
        elif num == '6':
            shuxing()  # 增加学生属性
        elif num == "7":
            chaxun()  # 查询所有学生信息
        elif num == '9':
            dgxuesheng()  # 查询单个学生信息
        elif num == '10':
            xiugai()  # 修改学生信息
        elif num == '0':
            print("退出系统")  # 退出系统
            exit()
        else:
            print("输入有误，请重新输入！")


# 1 创建文件夹功能
def wenjianjia():
    import os
    name = input("请输入您要创建的文件夹名：")

    if not os.path.exists(name):
        os.mkdir(name)
        print("创建成功")
        repeat()
    else:
        print("文件名已经存在！")
        repeat()


# 2 改变文件存储路径功能
def lujing():
    import os
    name = input("请输入您要修改的文件夹名：")
    list = os.listdir('./')
    if name in list:
        str = os.path.abspath(name)
        print("您要修改的文件夹现在位置：", str)
        str = input("请输入您要修改到的路径：")
        os.chdir(str)
        print("执行成功")
        repeat2()
    else:
        print("不存在此文件夹")
        repeat2()


# 3 读取学生名单功能
def mingdan():
    strp = "E:/untitled/.idea"
    file = open("C:/untitled/.idea/学生名单.txt", 'r')
    strlist = file.readlines()
    print("学生名单如下：")
    print(strlist)
    file.close()
    repeat3()


# 4.创建学生信息存储文本
def wenben():
    import os
    liststr = os.listdir('./')
    print("文件夹下的所有文件")
    for i in liststr:
        print(i)
    str1 = input("请输入您想要打开的文件夹:")

    if i in liststr:
        path1 = './' + str1
        os.chdir(path1)
        n = int(input("请输入学生人数:"))

        for i in range(n):
            strstu = input("请输入学生姓名：:")
            filename = strstu + '.txt'
            stu = open(filename, 'w')
            id = input("请输入学号：:")
            idstr = "sno:" + id + "\n"
            namestr = "student's name:" + strstu + '\n'
            grade = input("请输入学生班级:")
            gradestr = "student's grade:" + grade + '\n'
            stu.write(idstr)
            stu.write(namestr)
            stu.write(gradestr)
            stu.close()
            stu = open(filename, 'r')
            print(stu.read())
            stu.close()
            repeat4()
    else:
        print("there wasn't flie in here")
        repeat4()


# 5 增加学生详细信息功能:
def xsxinxi():
    strp = "C:/untitled/.idea"
    file = open("C:/untitled/.idea/学生名单.txt", 'r')
    strlist = file.readlines()
    lenght = len(strlist)
    print(strlist)

    for i in range(lenght):
        str1 = strlist[i]
        str = strp + str1[:-1] + "学生信息.txt"
        print(str)
        filestu = open(str, 'a')
        print("%s的家乡:" % (str1[:-1]))
        strinput = "的家乡：" + input("") + '\n'
        filestu.write(strinput)
        print("%s的评价" % (str1[:-1]))
        strinput = "评价：" + input("") + '\n'
        filestu.write(strinput)
        filestu.write("专业：软件技术\n")
        filestu.close()
        file.close()

    repeat5()


# 6 增加学生属性功能
def shuxing():
    strp = "C:/untitled/.idea"
    file = open("C:/untitled/.idea/学生名单.txt")
    strlist = file.readlines()
    lenght = len(strlist)
    print(strlist)

    for i in range(lenght):
        str1 = strlist[i]
        str = strp + str1[:-1] + "学生信息.txt"
        print(str)
        filestu = open(str, 'w')
        str2 = '姓名:' + str1
        filestu.write(str2)
        print("%s的爱好" % (str1[:-1]))
        strinput = "爱好:" + input("") + '\n'
        filestu.write(strinput)
        print("%s的成绩" % (str1[:-1]))
        strinput = "成绩：" + input("") + '\n'
        filestu.write(strinput)
        filestu.close()

    file.close()
    repeat6()


# 7 查询所有学生信息功能
def chaxun():
    import os
    str = os.getcwd()
    print(str)
    os.chdir("C:/untitled")
    str = os.getcwd()
    print(str)
    list = os.listdir()
    print("所有学生信息如下：")
    print(list)
    '''index=1
        while (index<len(list)):
        file=open(len(list),'r')
        l=file.readlines()
        print(l)
        index+=1
        file.close()*/'''
    repeat7()


# 8 查询单个学生信息功能
# 9 修改学生信息功能
def dgxuesheng():
    import os
    str = os.getcwd()
    print(str)
    os.chdir("C:/untitled")
    str = os.getcwd()
    print(str)
    list = os.listdir('./')
    print(list)
    list1 = input("请输入你要查看的学生：")

    if list1 in list:
        print(list1)
        file = open(list1, 'r')
        str2 = file.readlines()
        print(str2)
        file.close()
        repeat9()
    else:
        print("没有这个学生信息")
        repeat9()


# 10 退出系统
def xiugai():
    import os
    str = os.getcwd()
    print(str)
    os.chdir("C:/untitled")
    str = os.getcwd()
    print(str)
    list = os.listdir()
    print(list)
    stufind = input("您要查找的学生：")

    if stufind in list:
        stu = open(stufind, 'r')
        listxinxi = stu.readlines()

        for j in listxinxi:
            print(j[:-1])
        print("s" * 30)
        stu.close()
        stuo = open(stufind, 'w')
        update = input("您要修改的信息")
        updatav = input("值")

        for t in listxinxi:
            print(t[0:2])
            if update == t[:2]:
                t = update + ":" + updatav + '\n'
            stuo.write(t)
        stuo.close()
        stu = open(stufind, 'r')
        listxinxi = stu.readlines()

        for j in listxinxi:
            print(j[:-1])
        print("s" * 30)
        stu.close
    else:
        print("错了")
    repeat10()


def fanhui():
    while True:
        num = input("确定要退出吗？（Yes Or No,keepiing）")
        if num == "Yes":
            print("结束运行")
            break
        elif num == "no":
            main()
        else:
            print("输入有误，请重新输入！")



def repeat():
    while True:
        num = input("返回上一层，结束,继续:")
        if num == "结束":
            print("结束运行")
            break
        elif num == "no":
            main()
        elif num == "继续":
            wenjianjia()
        else:
            print("输入有误，请重新输入！")


def repeat2():
    while True:
        num = input("返回上一层，结束,继续:")
        if num == "结束":
            print("结束运行")
            break
        elif num == "no":
            main()
        elif num == "继续":
            lujing()
        else:
            print("输入有误，请重新输入！")


def repeat3():
    while True:
        num = input("返回上一层，结束,继续:")
        if num == "结束":
            print("结束运行")
            break
        elif num == "no":
            main()
        elif num == "继续":
            mingdan()
        else:
            print("输入有误，请重新输入！")


def repeat4():
    while True:
        num = input("返回上一层，结束,继续:")
        if num == "结束":
            print("结束运行")
            break
        elif num == "no":
            main()
        elif num == "继续":
            wenben()
        else:
            print("输入有误，请重新输入！")


def repeat5():
    while True:
        num = input("返回上一层，结束,继续:")
        if num == "结束":
            print("结束运行")
            break
        elif num == "no":
            main()
        elif num == "继续":
            xsxinxi()
        else:
            no()


def repeat6():
    while True:
        num = input("返回上一层，结束,继续:")
        if num == "结束":
            print("结束运行")
        elif num == "no":
            main()
        elif num == "继续":
            shuxing()
        else:
            print("输入有误，请重新输入！")


def repeat7():
    while True:
        num = input("返回上一层，结束,继续:")
        if num == "结束":
            print("结束运行")
            break
        elif num == "no":
            main()
        elif num == "继续":
            chaxun()
        else:
            print("输入有误，请重新输入！")


def repeat9():
    while True:
        num = input("返回上一层，结束,继续:")
        if num == "结束":
            print("结束运行")
            break
        elif num == "no":
            main()
        elif num == "继续":
            dgxuesheng()
        else:
            print("输入有误，请重新输入！")


def repeat10():
    while True:
        num = input("返回上一层，结束,继续:")
        if num == "结束":
            print("结束运行")
            break
        elif num == "no":
            main()
        elif num == "继续":
            xiugai()
        else:
            print("输入有误，请重新输入！")

if __name__ == '__main__':

    main()
