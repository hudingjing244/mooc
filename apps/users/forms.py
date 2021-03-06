# _*_ coding: utf-8 _*_
__author__ = "hudingjing"
__date__ = '2019/3/27 10:40 '

from django import forms
from captcha.fields import CaptchaField

from .models import UserProfile

class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password=forms.CharField(required=True,min_length=5)
    captcha = CaptchaField(error_messages={'invalid':u"验证码错误"})


class LoginForm(forms.Form):
    username=forms.CharField(required=True)
    password=forms.CharField(required=True,min_length=5)

class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid':u"验证码错误"})

class RestPwdForm(forms.Form):
    password1=forms.CharField(required=True,min_length=5)
    password2=forms.CharField(required=True,min_length=5)

class UploadImageForm(forms.ModelForm):

    class Meta:
        model=UserProfile
        fields=['image']

class UserInfoForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        #再次注意，前端form表单中的name字段必须和数据库中的field对应
        fields=['nick_name','birthday','gender','phone_num','address']

