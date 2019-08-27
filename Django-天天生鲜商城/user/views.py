import re
from datetime import datetime, timedelta

from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse


from cart.models import Cart
from goods.models import Goods, GoodsCategory
from user.form import RegisterForm, UserLoginForm
from user.models import UserToken

from utils.functions import get_random_ticket


def index(request):
    if request.method == 'GET':
        # 商品分类标题 图片
        goods_category = GoodsCategory.objects.all()

        # 各类商品前四条信息
        goods_type1 = Goods.objects.filter(category_id=1)[0:4]
        goods_type2 = Goods.objects.filter(category_id=2)[0:4]
        goods_type3 = Goods.objects.filter(category_id=3)[0:4]
        goods_type4 = Goods.objects.filter(category_id=4)[0:4]
        goods_type5 = Goods.objects.filter(category_id=5)[0:4]
        goods_type6 = Goods.objects.filter(category_id=6)[0:4]

        # 各类点击量前三条
        goods_type01 = Goods.objects.filter(category_id=1).order_by('-click_nums')[0:3]
        goods_type02 = Goods.objects.filter(category_id=2).order_by('-click_nums')[0:3]
        goods_type03 = Goods.objects.filter(category_id=3).order_by('-click_nums')[0:3]
        goods_type04 = Goods.objects.filter(category_id=4).order_by('-click_nums')[0:3]
        goods_type05 = Goods.objects.filter(category_id=5).order_by('-click_nums')[0:3]
        goods_type06 = Goods.objects.filter(category_id=6).order_by('-click_nums')[0:3]

        # 结果拼接，合并成字典
        goods_type = {
            'goods_type1': [goods_type1, goods_type01, goods_category[0]],
            'goods_type2': [goods_type2, goods_type02, goods_category[1]],
            'goods_type3': [goods_type3, goods_type03, goods_category[2]],
            'goods_type4': [goods_type4, goods_type04, goods_category[3]],
            'goods_type5': [goods_type5, goods_type05, goods_category[4]],
            'goods_type6': [goods_type6, goods_type06, goods_category[5]],
        }

        return render(request, 'web/index.html', {'goodstype': goods_type})


def register(request):
    if request.method == 'GET':
        return render(request, 'web/register.html')

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')

            password = form.cleaned_data.get('pwd1')
            email = form.cleaned_data.get('email')
            # make_password() 加密密码
            User.objects.create(username=username,
                                password=make_password(password),
                                email=email)
            # 返回登录
            return HttpResponseRedirect(reverse('user:login'))


        return render(request, 'web/register.html', {'form': form, 'data': form.data})


def login(request):
    if request.method == 'GET':
        data = request.COOKIES
        referrer = request.session.get('referrer')
        return render(request, 'web/login.html', {'data': data, 'referrer': referrer})

    if request.method == 'POST':

        # 验证提交表单
        form = UserLoginForm(request.POST)

        # 表单初步验证通过
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.filter(username=username).first()

            # 用户名 密码错误
            if not (user and check_password(password, user.password)):
                # 错误信息格式用的from表单的错误提示格式
                return render(request, 'web/login.html', {'form': {'errors':{'username':'账号或密码错误'}}})

            # 获取随机字符串
            token = get_random_ticket()
            out = datetime.now() + timedelta(hours=1)

        # todo：登录成功后跳转的url

            # 获取 中间件 保存的源url
            url = request.session.get('referrer')
            # 获取 登录界面 保存的源url
            url1 = request.POST.get('referrer')

            # 定义个res 不然会报未定义错误
            res = None
            if url:
                # 如果在购物车点了结算跳转到登录的
                if re.match('/order/place_order/', url):
                    res = HttpResponseRedirect(reverse('cart:cart'))
                # 其他中间件拦截的源url可以直接跳转回去
                elif url:
                    res = redirect(url)
            else:
                # 如果直接访问登录界面或者是注册界面跳转过来的
                if re.match('.*/user/login/', url1) or re.match('.*/user/register/', url1) or url1 == '':
                    res = HttpResponseRedirect(reverse('user:index'))
                # 其他方式访问的登录界面
                else:
                    # 如果获取不到session就用login页面获取的源url
                    res = HttpResponseRedirect(url1)

            # 向cookie中保存token参数 设置过期时间
            res.set_cookie('token', token, max_age=2*60*60)
            # 保存到数据库 如果存在则修改，如果不存在则创建
            user_ticket = UserToken.objects.filter(user=user).first()
            if user_ticket:
                # 更新user_ticket表数据
                user_ticket.token = token
                user_ticket.out_time = out
                user_ticket.save()
            else:
                # 创建user_token表数据
                UserToken.objects.create(user=user, username=user, token=token, out_time=out)

            # 是否点击了记住用户，是就在保存一份token
            remember = request.POST.get('remember')
            if remember == 'on':
                res.set_cookie('username', username)

         # todo：登录后本地购物车如果保存数据则保存到数据库

            try:
                # session里是否有商品？没有数据会报错   若有则存入数据库
                ses_goods = dict(request.session.get('goods'))
                if ses_goods:
                    for id, num in ses_goods.items():
                        goods_id = str(id)
                        goods_num = int(num)

                        shop_carts = Cart()
                        goods = Goods.objects.filter(id=goods_id).first()

                        # 获取用户

                        # 获取购物车数据库内的id 和数量
                        shop_cart = Cart.objects.filter(user=user).all()
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
                            shop_carts.nums = int(shop_carts.nums) + int(goods_num)
                            shop_carts.goods = goods
                            shop_carts.user = user
                            shop_carts.save()

                        # 保存完session会自动过期
            except:
                pass

            return res

        # 表单验证没通过
        else:
            return render(request, 'web/login.html', {'form': form})

# todo：页面顶部需要加载的信息 是否登录，用户名，购物车商品数量
def is_login(request):
    if request.method == 'GET':
        # 获取登录用户
        token = request.COOKIES.get('token')
        user = UserToken.objects.filter(token=token).first()
        if user:
            code = 200
            user1 = user.username
            # 初始购物车数量是空，获取会报错
            try:
                # <QuerySet [{'nums': 24}, {'nums': 6}, {'nums': 6}, {'nums': 2}]>
                goods_count = sum([num['nums'] for num in Cart.objects.filter(user=user.user).values('nums')])
            except:
                goods_count = 0
        else:
            code = 300
            user1 = ''
            try:
                goods_count = sum([int(v) for k, v in dict(request.session['goods']).items()])
            except:
                goods_count = 0

        return JsonResponse({'code': code, 'user': user1, 'goods_count': goods_count})

# 退出登录
def logout(request):

    # 将cookie中的sessionid值删掉，并且数据库表中的数据删掉
    request.session.flush()
    token = request.COOKIES.get('token')
    user = UserToken.objects.filter(token=token).first()
    user.delete()

    return redirect('/user/login/')
