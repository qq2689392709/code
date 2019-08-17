from django import forms

from django.contrib.auth.models import User



# 注册验证
class RegisterForm(forms.Form):
    username = forms.CharField(required=True,max_length=20,min_length=3,
                               error_messages={
                                   'required':'注册用户名必填',
                                   'max_length':'用户名过长，最长不超过20个字符',
                                   'min_length':'用户名过短，最少不低于3个字符'
                               })
    pwd1 = forms.CharField(required=True, max_length=20, min_length=3,
                               error_messages={
                                   'required': '密码必填',
                                   'max_length': '密码过长，最长不超过20个字符',
                                   'min_length': '密码过短，最少不低于3个字符'
                               })
    pwd2 = forms.CharField(required=True,error_messages={
                                   'required': '验证密码必填'
                               })
    email = forms.CharField(required=True, error_messages={'required': '邮箱必填'})
    allow = forms.BooleanField(required=True, error_messages={'required': '请勾选同意'})

    def clean(self):
        # 用户名是否注册
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError({'username': '注册用户名已存在，请选择登录'})
        # 校验密码是否正确
        pwd1 = self.cleaned_data.get('pwd1')
        pwd2 = self.cleaned_data.get('pwd2')
        if pwd1 != pwd2:
            raise forms.ValidationError({'pwd2': '两次密码不一致'})
        return self.cleaned_data

# 登录验证
class UserLoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=20, error_messages={'required': '用户名必填'})
    password = forms.CharField(required=True, max_length=20, error_messages={'required': '密码必填'})

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        # 用户名不存在
        username = User.objects.filter(username=username).exists()
        if not username:
            raise forms.ValidationError({'username': '账号不存在，请去注册'})

        return self.cleaned_data

# 用户地址保存的表单验证
class UserAddressForm(forms.Form):
    signer_name = forms.CharField(required=True, error_messages={'required': '*收件人必填'})
    address = forms.CharField(required=True, error_messages={'required': '*详细地址必填'})
    signer_mobile = forms.CharField(required=True, error_messages={'required': '*收件人手机号码必填'})
    signer_postcode = forms.CharField(required=False)
