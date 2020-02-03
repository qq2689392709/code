import re
a = '''员工1	经理1
员工2	经理2
员工3	主管2
经理1	主管1
经理2	主管1
主管1	总监1
主管2	总监1
总监1	CTO'''
dict1 = {}
list1 = re.split(r'\s',a)
for i in range(0,len(list1),2):
    dict1[list1[i]] = list1[i+1]
print(dict1)
dict2 ={}
for k,v in dict1.items():
    k3 = k
    l1 = []
    while dict1.get(k3):
        l1.append(k3)
        k3 = dict1.get(k3)
    l1.append(k3)
    dict2[l1[0]] = l1[1:]
print(dict2)
for k,v in dict2.items():
    print(k,":",v,"等级为{}级".format(len(dict2.get(k))+1))