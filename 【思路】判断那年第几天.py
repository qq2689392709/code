
# 输入某年某月某日，判断这一天是这一年的第几天？
import datetime

year = int(input("请输入4位数的年份:"))
month = int(input("请输入月份:"))
day = int(input("请输入当月哪一天:"))

targetDay = datetime.date(year, month, day)
dayCount = targetDay - datetime.date(targetDay.year - 1 ,12, 31)

print("%s是 %s年的第%s天。"%(targetDay,year,dayCount.days))
