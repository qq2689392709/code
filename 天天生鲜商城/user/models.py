from django.contrib.auth.models import User
from django.db import models

from goods.models import Goods



class UserAddress(models.Model):
    """
    收货地址表
    """
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    province = models.CharField(max_length=100, default='', verbose_name='省份')
    city = models.CharField(max_length=100, default='', verbose_name='城市')
    district = models.CharField(max_length=100, default='', verbose_name='区域')
    address = models.CharField(max_length=100, default='', verbose_name='详细地址')
    signer_name = models.CharField(max_length=20, default='', verbose_name='签收人')
    signer_mobile = models.CharField(max_length=11, default='', verbose_name='电话')
    signer_postcode = models.CharField(max_length=11, default='', verbose_name='邮编')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        db_table = 'f_user_address'



class UserToken(models.Model):
    """
    token 登录状态
    """
    user = models.ForeignKey(User, verbose_name='用户F', on_delete=models.CASCADE)
    username = models.CharField(max_length=20, unique=True, null=True, blank=True)
    token = models.CharField(max_length=100, unique=True, null=False,
                             verbose_name='token标识符')
    out_time = models.DateTimeField(null=True)

    class Meta:
        db_table = 'f_token'




