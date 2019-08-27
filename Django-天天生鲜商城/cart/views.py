from django.contrib.auth.models import User
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render

from goods.models import Goods
from cart.models import Cart
from user.models import UserToken


# 添加商品到购物车中
def add_cart(request):
    if request.method == 'POST':
        # 获取商品的ID个数
        goods_id = str(request.POST.get('goods_id'))
        goods_num = int(request.POST.get('goods_num'))

        # 格式化 {'商品id', 商品数量}
        goods_dicr = {str(goods_id): int(goods_num)}

        # 购物车图标数量
        cart_goods_num = 0

        # 是否登录了，获取用户
        token = request.COOKIES.get('token')
        user = UserToken.objects.filter(token=token).first()

        # 已登录，添加进数据库
        if user:
            shop_carts = Cart()
            goods = Goods.objects.filter(id=goods_id).first()

            # 获取购物车数据库内的id 和数量
            shop_cart = Cart.objects.filter(user=user.user).all()
            shop_carts_nums = {str(g.goods_id): int(g.nums) for g in shop_cart}

            # 如果存在则则修改数量
            if goods_id in shop_carts_nums:
                for k, v in shop_carts_nums.items():
                    if k == goods_id:
                        carts = Cart.objects.filter(goods_id=goods_id).first()
                        carts.nums = int(v) + int(goods_num)
                        carts.save()
            # 不存在则创建
            else:
                shop_carts.nums = goods_num
                shop_carts.goods = goods
                shop_carts.user = User.objects.filter(username=user.username).first()
                shop_carts.save()

                cart_goods_num += 1


        # 没登录
        else:
            # 有session
            try:
                # 是否添加过该商品，如果没有session会报错执行except
                session = dict(request.session.get('goods'))

                # 有session 商品也以存在 {'商品id', 商品数量}
                if goods_id in session:
                    session[goods_id] += goods_num
                    request.session['goods'] = session

                # 有session 商品不存在
                else:
                    session.update(goods_dicr)
                    request.session['goods'] = session


            # 没有session
            except:
                request.session['goods'] = goods_dicr

            # 购物车商品数量，转字典 获取value sum求和
            cart_goods_num = sum([int(v) for k, v in dict(request.session['goods']).items()])

        return JsonResponse({'code': 200, 'cart_goods_num': cart_goods_num})


# 购物车
def cart(request):
    if request.method == 'GET':
        # 获取登录用户
        token = request.COOKIES.get('token')
        user = UserToken.objects.filter(token=token).first()

        # 有登录
        if user:
            # 购物车是否有商品
            try:
                # 获取购物车里商品id和数量，没商品会报错
                shop_cart = Cart.objects.filter(user=user.user).order_by('-add_time').all()
                shop_carts_nums = [[int(g.goods_id), int(g.nums)] for g in shop_cart]

                shop_carts_id = [g.goods_id for g in shop_cart]

                carts = []
                # 遍历商品id
                for id in shop_carts_id:
                    goods = Goods.objects.get(id=id)
                    good_dict = dict(model_to_dict(goods))
                    # 给商品详情表添加数量
                    for num in shop_carts_nums:
                        if good_dict['id'] == num[0]:
                            good_dict['num'] = num[1]

                    carts.append(good_dict)

            # 购物车没商品
            except:
                carts = []

            return render(request, 'web/cart.html', {'carts': carts})

        # 未登录
        if not user:
            try:
                # 从session中拿商品的id，获取不到会报错
                goods = dict(request.session.get('goods'))

                carts = []

                # 转字典添加内容
                for id, num in goods.items():
                    goods = Goods.objects.get(id=id)
                    good_dict = dict(model_to_dict(goods))

                    # 给商品详情添加 数量字段
                    good_dict['num'] = num

                    carts.append(good_dict)
            except:
                # 未加入购物车直接访问购物车返回空列表
                carts = []

            return render(request, 'web/cart.html', {'carts': carts})


# 修改购物车中数据
def change_session_goods(request):
    if request.method == 'POST':
        # 获取用户
        token = request.COOKIES.get('token')
        user = UserToken.objects.filter(token=token).first()

        # 获取商品的ID个数
        goods_id = request.POST.get('goods_id')
        goods_num = request.POST.get('goods_num')

        if user:
            # 获取购物车数据库内的id 和数量
            shop_cart = Cart.objects.filter(user_id=user.user_id).all()
            shop_carts_nums = {str(g.goods_id): int(g.nums) for g in shop_cart}

            # 如果存在则则修改数量
            if goods_id in shop_carts_nums:
                for k, v in shop_carts_nums.items():
                    if k == goods_id:
                        carts = Cart.objects.filter(goods_id=goods_id).first()
                        carts.nums = int(goods_num)
                        carts.save()
            return JsonResponse({'code': 200})

        # 没登录
        else:
            goods_session = dict(request.session.get('goods'))

            goods_nums = Goods.objects.get(id=goods_id)

            if int(goods_num) > int(goods_nums.goods_nums):
                return JsonResponse({'code': 301, 'error': '商品库存不足'})

            # 上面转字典后增加一个数量key
            goods_session[goods_id] = goods_num

            request.session['goods'] = goods_session

        return JsonResponse({'code': 200, 'goods': request.session['goods']})


# 删除数据库信息
def change_del_goods(request):
    if request.method == 'POST':
        good_id = request.POST.get('good_id')
        try:
            # 获取登录用户，不报错就是登录了
            token = request.COOKIES.get('token')
            user = UserToken.objects.filter(token=token).first().user
            try:
                Cart.objects.filter(user_id=user.user_id,goods_id=good_id).delete()
                return JsonResponse({'code': 200, 'msg': '删除成功'})
            except:
                return JsonResponse({'code': 301, 'msg': '商品不存在'})
        except:
            # 没登陆，获取session
            goods = dict(request.session.get('goods'))

            # 删除商品
            goods.pop(good_id)

            request.session['goods'] = goods

            return JsonResponse({'code': 200, 'msg': '请求成功，'})


# 修改购物车商品选中状态，准备创建订单
def is_select(request):
    if request.method == 'POST':
        try:
            # 获取用户
            token = request.COOKIES.get('token')
            user = UserToken.objects.filter(token=token).first().user

            # 转换为列表
            goods_list = eval(request.POST.get('goods_list_str'))

            # 初始化选中状态
            Cart.objects.filter(user=user).update(is_select=0)

            # 过滤 全部修改
            Cart.objects.filter(goods_id__in=goods_list).update(is_select=1)

        except:
            return JsonResponse({'code': 301, 'msg': '商品不存在'})

    return JsonResponse({'code': 200, 'msg': '请求成功'})
