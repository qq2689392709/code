from django.contrib import admin

# Register your models here.

from goods.models import GoodsCategory, Goods, GoodsImage

# 模型Article交给后台管理
admin.site.register(Goods)
admin.site.register(GoodsCategory)
admin.site.register(GoodsImage)
