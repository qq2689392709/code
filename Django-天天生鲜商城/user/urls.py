from django.urls import path, re_path

from user.views import index, register, login, is_login, logout

urlpatterns = [

    # 主页
    path('index/', index, name='index'),
    # 注册
    path('register/', register, name='register'),
    # 登录
    path('login/', login, name='login'),
    # 继承页面需要获取的信息
    path('is_login/', is_login, name='is_login'),
    # 退出登录
    path('logout/', logout, name='logout'),

]
