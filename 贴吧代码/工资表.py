import copy

salary_list = []


def salary_add():
    ## 一次性输入一行信息，用split()切割内容
    staff = input('【按照格式，用空格隔开】姓名 基本工资 奖金 应扣工资:').split()
    salary_list.append({'姓名': staff[0], '基本工资': int(staff[1]), '奖金': int(staff[2]), '应扣工资': int(staff[3])})
    print('添加成功')

    for i in salary_list:
        print(i)


def salary():
    # enumerate() 生成元素对应的下标，copy.deepcopy()需要修改原列表建议对原列表进行拷贝，你也可以不用
    for index, staff_dict in enumerate(copy.deepcopy(salary_list)):
        # 根据下标对指定的字典内插入新的键值对
        salary_list[index]['实际工资'] = staff_dict['基本工资'] + staff_dict['奖金'] + staff_dict['应扣工资']

    print('实际工资结算完成')

    for i in salary_list:
        print(i)


def salary_save():
    # with 上下文管理器，自动关闭文件保存。w和a模式是写入，文件不存在则创建
    with open('salary.txt', 'w', encoding='UTF-8')as f:
        f.write(str(salary_list))

    print('保存完成')

def main():
    while True:
        print('\n***************************************')
        print('1、添加员工\t2、工资结算\t3、工资单保存\t4、退出')
        num = input('请选择：')
        if num == '1':
            salary_add()
        elif num == '2':
            salary()
        elif num == '3':
            salary_save()
        elif num == '4':
            exit()
        else:
            print('选择有误，请重新选择')


if __name__ == '__main__':
    main()
