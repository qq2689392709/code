from django.contrib import admin

# Register your models here.

from order.models import OrderGoods, OrderInfo

# 模型Article交给后台管理
admin.site.register(OrderGoods)
admin.site.register(OrderInfo)
