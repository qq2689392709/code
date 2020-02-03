import os
import shutil

def classify(path):
    path = os.curdir if path == '' else path
    for file in os.listdir(path):
        # 后缀
        suffix = os.path.splitext(file)[1]
        # 文件夹后缀为空，忽略
        if suffix != '':
            # 原文件路径
            path_abs = os.path.join(path, file)
            # 新文件路径
            path_nwe = os.path.join(path, suffix[1:])
            # 创建文件夹
            None if os.path.exists(path_nwe) else os.mkdir(path_nwe)
            # 转移文件
            shutil.move(path_abs, path_nwe) if not os.path.exists(os.path.join(path_nwe,file)) else print(f'文件重名：{path_abs}')
    # 打开文件夹窗口
    os.system(f"start explorer {path}")

path = input('请输入文件夹路径[默认当前路径]:')
classify(path)


