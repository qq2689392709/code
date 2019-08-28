# 母亲节,每年的5月第二个周末
import calendar


year = int(input('年份:'))
# 日历模块直接查询5月
month = calendar.month(year, 5)
print(month)

# 按行切割后取第二周最后一天
month_day = month.split('\n')[3].split()[-1]
print(f'母亲节:{year}-5-{month_day}')
