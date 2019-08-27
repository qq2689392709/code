#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tinatian.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

'''
购物车：
    未登录-->访问 商品添加 购物车数量 数量增减 选中 小计 总计 
            登录后把本地添加进数据库
            
    登录---->同上
商品：
    分类 列表 详情 数量增减 直接修改数量 加入购物车 分页 页码选中 排序 搜索 分词搜索
用户：
    注册 登录 记住用户 用户中心 收货地址 创建订单 订单中心 支付(x)
主页：
    未登录提示 登录限时 图片加载 分类跳转 查看更多 全部商品 图片全部链接详情 

'''
