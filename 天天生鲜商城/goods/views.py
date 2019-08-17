from datetime import datetime

import jieba
from django.shortcuts import render

from goods.models import Goods, Click, GoodsCategory
from user.models import UserToken


def goods_detail(request, id):

    # 商品点击量 +1
    goods = Goods.objects.filter(id=id).first()
    goods.click_nums += 1
    goods.save()

    # 获取前三个新品
    goods_new = Goods.objects.filter(is_new=1).all()[0:3]

    # 登录保存浏览记录
    try:
        # 获取登录用户
        token = request.COOKIES.get('token')
        user = UserToken.objects.filter(token=token).first().user

        # 获取商品id
        goods_id = Goods.objects.get(id=id)

        # 获取浏览记录是否存在
        tf = Click.objects.filter(user=user, goods_id_id=goods_id).all()

        # 存在则修改时间
        if tf:
            tf.update(add_time=datetime.now())
        # 不存在则添加
        if not tf:
            Click.objects.create(user=user, goods_id=goods_id)

        # 只保存5条浏览记录，多出几条循环几次
        len_ = len(Click.objects.filter(user=user).all())
        if len_ > 5:
            # 循环。防止数据条数异常
            for i in range(len_ - 5):
                # 删除最先添加的第一条
                Click.objects.filter(user=user).order_by('add_time').first().delete()

    except:
        # 未登录
        pass

    return render(request, 'web/detail.html', {'goods': goods, 'goods_new': goods_new})


def list(request, **kwargs):
    # sort=排序 0=无 1=价格升序 2=价格降序
    # type=类型 1-6 非数字就是搜索内容
    # page=页码

    sort = int(kwargs['sort'])
    page = int(kwargs['page'])

    # 先定义，下面代码不会黄色警告
    type = None         # 页码或者搜索内容
    search = None       # 搜索内容
    goods_list1 = []    # 商品列表
    goods_category = 0  # 商品分类

# TODO: type是数字的话正常获取分类
    if str(kwargs['type']).isdigit():
        type = int(kwargs['type'])

        # 0=全部商品
        if type == 0:
            goods_category = 0
            goods_list1 = Goods.objects.all()
            if sort == 1:
                goods_list1 = Goods.objects.order_by('shop_price')
            if sort == 2:
                goods_list1 = Goods.objects.order_by('-shop_price')

        if type in [1, 2, 3, 4, 5, 6]:
            # 商品分类从 1 开始
            goods_category = GoodsCategory.objects.all()[type - 1]
            for type1 in goods_category.CATEGORY_TYPE:
                if type == int(type1[0]):
                    goods_category = type1[1]

            goods_list1 = Goods.objects.filter(category_id=type).all()

            if sort == 1:
                goods_list1 = Goods.objects.filter(category_id=type).order_by('shop_price')
            if sort == 2:
                goods_list1 = Goods.objects.filter(category_id=type).order_by('-shop_price')

# TODO：搜索页面
    else:
        # 非数字的话是type搜索内容
        type = str(kwargs['type'])
        search = type
        # jieba 模块全模式,分词搜索
        participle = jieba.cut(type,cut_all=True)


        for par_goods in participle:
            if par_goods != '':
                goods = Goods.objects.filter(name__contains=par_goods).all()
                for i in goods:
                    if i not in goods_list1:
                        goods_list1.append(i)

        # 排序
        if sort == 1:
            goods_list1 = sorted(goods_list1,key=lambda x:x.shop_price)
        if sort == 2:
            goods_list1 = sorted(goods_list1,key=lambda x:x.shop_price,reverse=True)

        # 商品分类
        goods_category = 0


    # 获取三条新品
    goods_new = Goods.objects.filter(is_new=1).all()[0:3]

    # 分组 20个商品 一组
    cart_data_list = [goods_list1[i:i + 20] for i in range(0, len(goods_list1), 20)]

    # 防下标(页码)越界
    if page > len(cart_data_list):
        page = len(cart_data_list)
    if page < 1:
        page = 1

    # 获取页码对应的商品
    if cart_data_list != []:
        goods_list = cart_data_list[page - 1]
    else:
        goods_list = []

    cart_data_len = range(1, len(cart_data_list) + 1)

    return render(request, 'web/list.html', {'goods_list': goods_list, 'goods_new': goods_new, 'type': type,
                                             'goods_category': goods_category, 'page': page, 'page1': cart_data_len,
                                             'page_up': page - 1, 'page_down': page + 1, 'sort': sort,'search':search})


