import re
from datetime import datetime

from django.db.models import Q
from django.http import request
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

from user.models import UserToken


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):


        # 不需要验证url地址
        not_need_login = ['/user/(.*)', '/goods/(.*)',
                          '/media/(.*)', '/cart/(.*)','/admin/(.*)']
        # 获取当前访问url的地址
        path = request.path

        # 当访问首页的时候，直接去主页
        if path == '/':
            return redirect('user:index')

        # 判断如果请求地址为不需要登录验证的地址，则返回None
        for not_need_path in not_need_login:
            if re.match(not_need_path, path):
               return None

        # 先获取cookies中的ticket参数
        token = request.COOKIES.get('token')
        # 如果没有ticket，则直接跳转到登录
        if not token:
            # 先保存当前url
            request.session['referrer'] = path
            return redirect('user:login')

        user_ticket = UserToken.objects.filter(token=token).first()
        if user_ticket:
            # 获取到有认证的相关信息
            # 1. 验证当前认证信息是否过期，如果没过期，request.user赋值
            # 2. 如果过期了，跳转到登录，并删除认证信息
            if datetime.utcnow() > user_ticket.out_time.replace(tzinfo=None):
                # 过期
                UserToken.objects.filter(user=user_ticket.user).delete()

                request.session['referrer'] = path
                return redirect('user:login')
            else:
                # 没有过期，赋值request.user，并且删除多余的认证信息
                request.user = user_ticket.username
                UserToken.objects.filter(Q(username=user_ticket.username) & ~Q(token=token)).delete()

                return None
        else:
            request.session['referrer'] = path
            return redirect('user:login')

