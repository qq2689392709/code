from django.contrib import admin

# Register your models here.

from cart.models import Cart

# 模型Article交给后台管理
admin.site.register(Cart)
