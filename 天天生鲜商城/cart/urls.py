from django.urls import path

from cart.views import add_cart, cart, change_session_goods, change_del_goods, is_select

urlpatterns = [
    path('cart/', cart, name='cart'),
    # 添加
    path('add_cart/', add_cart, name='add_cart'),
    # 修改数量
    path('change_session_goods/', change_session_goods, name='change_session_goods'),
    # 删除
    path('change_del_goods/', change_del_goods, name='change_del_goods'),
    # 修改选中状态
    path('is_select/', is_select, name='is_select'),

]
