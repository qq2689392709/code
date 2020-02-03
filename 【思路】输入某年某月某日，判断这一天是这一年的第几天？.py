
# 输入某年某月某日，判断这一天是这一年的第几天？
import datetime

y = int(input("请输入4位数字的年份:"))
m = int(input("请输入月份:"))
d = int(input("请输入是哪一天"))

targetDay = datetime.date(y,m,d)
dayCount = targetDay - datetime.date(targetDay.year -1,12,31)

print("%s是 %s年的第%s天。"%(targetDay,y,dayCount.days))
