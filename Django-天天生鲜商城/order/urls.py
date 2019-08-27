from django.urls import path, re_path

from order.views import place_order, user_center_order, user_center_site, user_center_info, user_center_site_alter, \
    user_change_password, center

urlpatterns = [
    # 创建订单
    re_path('^place_order/', place_order, name='place_order'),
    # 用户中心
    path('user_center_info/', user_center_info, name='user_center_info'),
    # 我的订单
    path('user_center_order/', user_center_order, name='user_center_order'),
    # 收获地址
    path('user_center_site/', user_center_site, name='user_center_site'),
    # 修改 删除地址
    path('user_center_site_alter/<int:id>', user_center_site_alter, name='user_center_site_alter'),
    path('center/', center, name='center'),
    # 修改密码
    path('user_change_password/', user_change_password, name='user_change_password')
]
