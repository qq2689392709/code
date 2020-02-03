def count_time(func):
    def int_time(x,y):
        end_time = datetime.datetime.now()
        print('运行了{}，结果：{}'.format(func.__name__,func(x,y)))
        print(f'运行时间：{datetime.datetime.now()-end_time}')
    return int_time


@count_time
def add(x,y):
    for i in range(1000):
        for j in range(1000):
            pass
    return x+y
