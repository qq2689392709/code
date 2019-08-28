# 文件单词替换


name = input('请输入文件名：')
first = input('请输入需要替换的单词或字符：')
new = input('请输入新的单词或字符：')

with open(name,'r',encoding='UTF-8') as f:
    file = f.read()

yes_no = input(f'\n文件 {name} 中共有{file.count(first)}个【{first}】\n您确定要把所有的【{first}】替换为【{new}】吗？\n【YES/NO】：')

if yes_no == 'yes':
    with open(name,'w',encoding='UTF-8') as f:
        f.write(file.replace(first,new))
