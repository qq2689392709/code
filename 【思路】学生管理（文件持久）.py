import os
import shutil
import time


class student():
    # 默认文件名
    name_ = '学生信息'

    # 获取工作路径
    def path(self):

        # 获取当前文件的所在路径，分开路径和文件名
        a_path, b = os.path.split(os.path.realpath(__file__))
        if os.path.exists('%s\\path.txt' % a_path):
            # 获取路径里的path文件
            path = open('%s\\path.txt' % a_path, 'r')
            path_str = path.readlines()
            path.close()
            print(path_str)
            # 如果不是空的，按文件内路径修改工作路径
            if path_str != []:
                self.name_ = path_str[0].strip('\n')
                os.chdir(path_str[1])

        # 获取不到的话创建一个默认文件
        else:
            # 如果默认文件夹不存在则创建
            if not os.path.exists('%s\\%s.txt' % (a_path, self.name_)):
                os.makedirs(self.name_)

            open("./%s/学生名单.txt" % self.name_, 'w')
            path = open('%s\\path.txt' % a_path, 'w')
            path.write("%s\n%s" % (self.name_, os.getcwd()))
            path.close()

    # 开始部分
    def print_menu(self):
        while True:
            print()
            print("=" * 30)
            print("学生管理系统")
            print("1.创建文件夹功能")
            print("2.改变文件存储路径功能")
            print("3.读取学生名单功能")
            print("4.创建学生信息存储文本")
            print("5.增加学生详细信息功能")
            print("6.增加学生属性功能")
            print("7.查询所有学生信息功能")
            print("8.查询单个学生信息功能")
            print("9.修改学生信息功能")
            print("10.退出系统")

            key = input("请选择功能（序号）：")

            if key == '1':  # 创建文件夹
                self.establishFile()
            elif key == '2':  # 改变文件存储路径功能
                self.amendFile()
            elif key == '3':  # 读取学生名单功能
                self.readStu()
            elif key == '4':  # 创建学生信息存储文本
                self.establishStu()
            elif key == '5':  # 增加学生详细信息功能
                self.addStu()
            elif key == '6':  # 增加学生属性功能
                self.addStuAtt()
            elif key == '7':  # 查询所有学生信息功能
                self.inquireAll()
            elif key == '8':  # 查询单个学生信息功能
                self.inquireSingle()
            elif key == '9':  # 修改学生信息功能
                self.amendSingle()
            elif key == '10':  # 退出系统
                self.out()

    # 创建文件夹
    def establishFile(self):

        name = input("请输入您要创建的文件夹名：")
        if name == '':
            return
        self.name_ = name

        path1 = os.path.exists(self.name_)
        # 判断是否存在文件夹如果不存在则创建为文件夹
        if not path1:
            os.makedirs(self.name_)  # makedirs 创建文件时如果路径不存在会创建这个路径
            a_path, b = os.path.split(os.path.realpath(__file__))
            path = open('%s\\path.txt' % a_path, 'w')
            path.write(self.name_ + '\n' + os.path.abspath(self.name_))
            path.close()
            print("【%s】创建成功" % self.name_)
        else:
            print("已经存在")

        # 创建文件后继续创建个学生名单
        a = open("./%s/学生名单.txt" % self.name_, 'w')
        a.close()

        # 暂停1秒
        time.sleep(1)
        return

    # 改变文件存储路径功能
    def amendFile(self):

        # 获取当前工作路径
        str2 = os.path.abspath(self.name_)
        print("当前保存路径：", str2)

        str1 = input("请输入新的路径：")
        # 如果没输入路径就返回
        if str1 == '':
            return

        # 新路径文件夹不存自动创建,确保数据迁移
        if not os.path.exists(str1):
            os.makedirs(str1)

        # 保存新的储存信息的文件夹名和工作路径
        a_path, b = os.path.split(os.path.realpath(__file__))
        path = open('%s\\path.txt' % a_path, 'w')
        path.write(self.name_ + '\n' + str1)
        path.close()

        # 原文件转移到新路径上，改变工作路径
        shutil.move(str2, str1)
        os.chdir(str1)

        print("执行成功当前路径：", os.getcwd())  # 显示当前路径

        time.sleep(1)
        return

    # 读取学生名单功能
    def readStu(self):

        path = "./%s/学生名单.txt" % self.name_
        file = open(path, 'r')
        strlist = file.readlines()
        for info in strlist:
            info_dict = eval(info)
            print('学号：%s\t姓名：%s\t班级：%s' % (info_dict['学号'], info_dict['姓名'], info_dict['班级']))

        file.close()
        time.sleep(1)
        return

    # 创建学生信息存储文本
    def establishStu(self):

        desktop_path = "./%s/学生名单.txt" % self.name_
        name = input('学生名字：')
        grade = input('学生班级：')

        a1 = open(desktop_path, 'r')
        a2 = a1.readlines()

        # 获取最大的学号号码
        file_list = sorted(a2, key=lambda x: eval(x.strip('\n'))['学号'], reverse=True)
        file_len = eval(file_list[0])['学号']
        a1.close()

        # 学号为现在学生的数量
        file = open(desktop_path, 'a')
        file.write('{"学号":%s,"姓名":"%s","班级":"%s"}\n' % (file_len + 1, name, grade))

        full_path = './%s/' % self.name_ + name + '.txt'
        file1 = open(full_path, 'w')
        file1.write('{"学号":%s,"姓名":"%s","班级":"%s"}' % (file_len + 1, name, grade))

        file.close()
        file1.close()

        print('添加成功')
        time.sleep(0.5)

        return

    # 增加学生详细信息功能
    def addStu(self):
        # 添加学生信息

        path = "%s\\%s\\学生名单.txt" % (os.getcwd(), self.name_)
        file = open(path, 'r')
        stu_list = file.readlines()
        id = int(input("请输入学生学号："))
        for i in stu_list:
            i = eval(i)
            if i['学号'] == id:
                age = input("请输入学生年龄：")
                height = input("请输入学生身高：")
                weight = input("请输入学生体重：")
                i['年龄'] = age
                i['身高'] = height
                i['体重'] = weight

                path = '%s\\%s\\' % (os.getcwd(), self.name_) + i['姓名'] + '.txt'
                file1 = open(path, 'w')
                file1.write(str(i))
                file1.close()

                print("添加成功")
                return

        print('找不到改学号的学生')

        file.close()

        time.sleep(1)
        return

    # 增加学生属性功能
    def addStuAtt(self):

        list = os.listdir('./%s/' % self.name_)
        print(list)
        mod_name = input("请输入你要增加信息的学生姓名：")
        if mod_name + '.txt' in list:
            file = open('./%s/%s.txt' % (self.name_, mod_name), 'r')
            student = eval(file.readline())
            file.close()
            for k, v in student.items():
                print('%s：%s' % (k, v))

            jia = input('%s的家乡：' % mod_name)
            pingjia = input('%s的评价：' % mod_name)
            student['家乡'] = jia
            student['评价'] = pingjia

            file1 = open('./%s/%s.txt' % (self.name_, mod_name), 'w')
            print(student)
            file1.write(str(student))
            file1.close()
            print('添加成功')
        else:
            print('找不到该学生信息')

        time.sleep(1)
        return

    # 查询所有学生信息功能
    def inquireAll(self):

        path = "./%s/学生名单.txt" % self.name_
        file = open(path, 'r')
        strlist = file.readlines()

        if strlist == []:
            print('当前无信息记录')

        for info in strlist:
            info_dict = eval(info)
            print('学号：%s\t姓名：%s\t班级：%s' % (info_dict['学号'], info_dict['姓名'], info_dict['班级']))



        file.close()
        time.sleep(1)
        return

    # 查询单个学生信息功能
    def inquireSingle(self):

        list = os.listdir('./%s/' % self.name_)
        mod_name = input("请输入你要查询的学生姓名：")
        if mod_name + '.txt' in list:
            file = open('./%s/%s.txt' % (self.name_, mod_name), 'r')
            student = eval(file.readline())
            file.close()
            for k, v in student.items():
                print('%s: %s' % (k, v))

        else:
            print("找不到该学生信息")

        time.sleep(1)
        return

    # 修改学生信息功能
    def amendSingle(self):

        list = os.listdir('./%s/' % self.name_)
        mod_name = input("请输入你要查询的学生姓名：")
        if mod_name + '.txt' in list:
            file = open('./%s/%s.txt' % (self.name_, mod_name), 'r')
            student = eval(file.readline())
            file.close()
            for k, v in student.items():
                print('%s: %s' % (k, v))

            ke = input('修改哪个：')
            if ke in student.keys():
                valu = input('请输入新的内容：')
                student[ke] = valu
                print(student[ke])

                file1 = open('./%s/%s.txt' % (self.name_, mod_name), 'w')
                file1.write(str(student))
                file1.close()
                print('修改成功')
            else:
                print('输入有误')

        else:
            print("找不到该学生信息")

            self.establishFile()

        time.sleep(1)
        return

    # 退出系统
    def out(self):
        quit_confirm = input("亲，真的要退出吗？（yes or no):")
        if quit_confirm == "yes":
            print('退出系统')
        else:
            print("输入有误，请重新输入")


if __name__ == '__main__':
    s = student()
    s.path()
    s.print_menu()
