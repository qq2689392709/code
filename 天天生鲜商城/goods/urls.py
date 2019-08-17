from django.urls import path, re_path

from goods.views import goods_detail, list

urlpatterns = [
    # 商品详情页
    path('goods_detail/<int:id>/', goods_detail, name='goods_detail'),
    # 商品列表和搜索
    re_path(r'list/(?P<sort>\d+)/(?P<type>.*)/(?P<page>\d+)/', list, name='list'),

]
