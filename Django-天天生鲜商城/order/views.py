from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render

from cart.models import Cart
from goods.models import Click, Goods
from order.models import OrderInfo, OrderGoods
from user.form import UserAddressForm
from user.models import UserAddress, UserToken

from utils.functions import get_order_sn, get_trade_no


# 创建订单
def place_order(request):
    if request.method == 'GET':

        # 获取商品信息
        carts = []

        # 商品总数量
        goods_count = 0

        # 获取登录用户
        token = request.COOKIES.get('token')
        user = UserToken.objects.filter(token=token).first().user

        # 用户地址信息
        user_addresses = UserAddress.objects.filter(user=user).all()


        try:
            # 获取token，如果是商品详情点了立即购买
            cart_id = request.GET.get('goods_id')
            cart_num = int(request.GET.get('goods_num'))

            # 从立即购买跳转来的
            if cart_id:
                goods = Goods.objects.get(id=cart_id)
                goods_ = dict(model_to_dict(goods))
                goods_['num'] = cart_num
                goods_['sum'] = cart_num * goods_['shop_price']
                carts.append(goods_)

                goods_count = cart_num

                # 加入购物车
                shop_carts = Cart()
                shop_carts.nums = cart_num
                shop_carts.goods = Goods.objects.filter(id=cart_id).first()
                shop_carts.user = User.objects.filter(username=user.username).first()
                shop_carts.is_select = 1
                shop_carts.save()


        # 如果空的话 按购物车选中商品创建订单
        except:
            cart_is = Cart.objects.filter(is_select=1).all()

            for cart in cart_is:
                goods = Goods.objects.get(id=cart.goods_id)
                goods_ = dict(model_to_dict(goods))
                # 转字典添加数量key
                goods_['num'] = cart.nums
                goods_['sum'] = cart.nums * goods_['shop_price']
                carts.append(goods_)

            goods_count = sum([i.nums for i in cart_is])


        # 商品总价格
        goods_sum = sum([i['num'] * i['shop_price'] for i in carts])

        return render(request, 'web/place_order.html', {'user_addresses': user_addresses, 'carts': carts,
                                                    'goods_count': goods_count, 'goods_sum': goods_sum})



    if request.method == 'POST':
        site_id = int(request.POST.get('site'))
        pay = int(request.POST.get('pay'))

        # 获取登录用户
        token = request.COOKIES.get('token')
        user = UserToken.objects.filter(token=token).first().user

        # 商品信息
        carts = []
        cart_is = Cart.objects.filter(is_select=1).all()

        for cart in cart_is:
            goods = Goods.objects.get(id=cart.goods_id)
            goods_ = dict(model_to_dict(goods))
            # 转字典添加数量key
            goods_['num'] = cart.nums
            carts.append(goods_)

        # 总价格和 +10 邮费   全不包邮
        goods_sum = sum([i['num'] * i['shop_price'] for i in carts]) + 10

        # 地址表
        address = UserAddress.objects.filter(id=site_id).first()

        # 获取订单号 交易号
        order_sn = get_order_sn()
        order = OrderInfo()

        # 保存信息
        order.user = user
        order.order_sn = order_sn
        order.trade_no = get_trade_no()
        order.order_mount = goods_sum
        order.address = address.address
        order.signer_name = address.signer_name
        order.signer_mobile = address.signer_mobile
        order.save()

        # 保存关联的详情表
        for i in cart_is:
            or_goods = OrderGoods()
            or_goods.order = OrderInfo.objects.filter(user=user).first()
            or_goods.order_sn = order_sn
            or_goods.goods = Goods.objects.filter(id=i.goods_id).first()
            or_goods.goods_nums = i.nums
            or_goods.save()

            # 修改商品库存
            i.goods.goods_nums -= i.nums
            i.save()

        # 删除已下单的商品
        cart_is.delete()

        return JsonResponse({'code': 200, 'msg': '请求成功'})


# 我的订单
def user_center_order(request):
    if request.method == 'GET':
        # 获取分页
        try:
            # 转化为int类型，默认page为1
            page = int(request.GET.get('page', 1))
        except:
            # 页码异常强制等于1
            page = 1

        # 获取登录用户
        token = request.COOKIES.get('token')
        user = UserToken.objects.filter(token=token).first().user

        # 获取当前用户所有的订单信息和关联表
        order_info = OrderInfo.objects.filter(user=user).order_by('-add_time').all()
        order_status = OrderInfo.ORDER_STATUS

        # 一条订单一个字典，[{对象:[商品详情]}]套列表，保存顺序
        dindan = []
        for i in order_info:
            order_goods_dict = {}
            order_goods = []
            # 商品详情转字典格式添加 数量 单样总价 全部总价
            # order_good = 同一条订单里是商品信息
            order_good = OrderGoods.objects.filter(order_sn=i.order_sn).all()

            # 获取订单包含的全部商品信息
            for goods in order_good:
                goods1 = dict(model_to_dict(goods.goods))
                # <class 'dict'>: {'id': 7, 'category': 1, 'name': '草莓', 'goods_sn':
                # 添加 【数量】 【单个总价】 【全部总价】 信息
                goods1['goods_nums'] = goods.goods_nums
                goods1['goods_sum'] = goods1['goods_nums'] * goods1['shop_price']
                goods1['goods_sums'] = goods1['goods_nums'] * goods1['goods_sum']
                # 存进列表
                order_goods.append(goods1)

            # 存成一个字典，{对象:[商品详情]}
            order_goods_dict[i] = order_goods

            # 在添加进列表保存顺序，[{对象:[商品详情]}]
            dindan.append(order_goods_dict)

        # 处理完数据开始分页
        paginator = Paginator(order_info, 2)
        pages = paginator.page(page)

        # 分页内容
        dindan = dindan[(page - 1) * 2:page * 2]

        return render(request, 'web/user_center_order.html',
                      {'dindan': dindan, 'order_status': order_status, 'pages': pages})


# 收货地址 新增地址
def user_center_site(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        # 获取登录用户
        token = request.COOKIES.get('token')
        user = UserToken.objects.filter(token=token).first().user

        if not id:
            user_addresses = UserAddress.objects.filter(user=user).order_by('-id')
            return render(request, 'web/user_center_site.html', {'user_addresses': user_addresses})

        user_addresses = UserAddress.objects.filter(user=user,id=int(id)).first()
        user_dict = dict(model_to_dict(user_addresses))
        return JsonResponse({'code':200,'msg':'请求成功','data':user_dict})

    if request.method == 'POST':
        # 地址验证
        form = UserAddressForm(request.POST)

        # 获取登录用户
        token = request.COOKIES.get('token')
        user = UserToken.objects.filter(token=token).first().user

        if form.is_valid():

            address_info = form.cleaned_data
            # 添加地址
            UserAddress.objects.create(**address_info, user=user)

            # 重新获取地址表
            user_addresses = UserAddress.objects.filter(user=user).order_by('-id')

            return render(request, 'web/user_center_site.html', {'user_addresses': user_addresses})
        else:

            user_addresses = UserAddress.objects.filter(user=user).order_by('-id')
            return render(request, 'web/user_center_site.html', {'form': form, 'user_addresses': user_addresses})

# 修改 删除地址
def user_center_site_alter(request,id):
    if request.method == 'POST':
        # <QueryDict: {'signer_name': ['小花'], 'address': ['湖北省长沙市']
        # 处理格式
        post = {k:v[0] for k,v in dict(request.POST).items()}
        UserAddress.objects.filter(id=id).update(**post)
        return JsonResponse({'code':200,'msg':'请求成功'})

    # 删除地址
    if request.method == 'DELETE':
        UserAddress.objects.filter(id=id).delete()
        return JsonResponse({'code': 200, 'msg': '请求成功'})

# 快速新增地址
def center(request):
    if request.method == 'POST':
        form = UserAddressForm(request.POST)
        token = request.COOKIES.get('token')
        user = UserToken.objects.filter(token=token).first().user
        if form.is_valid():
            address_info = form.cleaned_data
            UserAddress.objects.create(**address_info, user=user)
            return JsonResponse({'code':200})
        else:
            return JsonResponse({'code':500})



# 用户中心
def user_center_info(request):
    if request.method == 'GET':
        # 获取登录用户
        token = request.COOKIES.get('token')
        user = UserToken.objects.filter(token=token).first().user

        # 获取一条地址
        user_resses = UserAddress.objects.filter(user=user).first()

        # 获取游览记录
        goods_list = [goods.goods_id for goods in Click.objects.filter(user=user).order_by('-add_time').all()]

        return render(request, 'web/user_center_info.html', {'user_resses': user_resses, 'goods_list': goods_list})

# 修改密码
def user_change_password(request):
    if request.method == 'POST':
        pwd = request.POST.get('pwd')
        pwd1 = request.POST.get('pwd1')
        pwd2 = request.POST.get('pwd2')

        # 获取用户
        token = request.COOKIES.get('token')
        user = UserToken.objects.filter(token=token).first().user

        # 获取密码对比原始密码
        if check_password(pwd, user.password):
            if pwd1 == pwd2:
                if pwd != pwd1:
                    user_pwd = User.objects.filter(id=user.id).first()
                    user_pwd.password = make_password(pwd1)
                    user_pwd.save()
                    return JsonResponse({'code': 200, 'data': '修改成功'})
                else:
                    return JsonResponse({'code': 601, 'data': '新密码与原密码一致'})
            return JsonResponse({'code': 602, 'data': '新密码不一致'})
        return JsonResponse({'code': 603, 'data': '密码错误'})
