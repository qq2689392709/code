from django.contrib import admin

# Register your models here.

from user.models import UserAddress, UserToken


# 模型Article交给后台管理
admin.site.register(UserAddress)
admin.site.register(UserToken)

