# _*_ coding: utf-8 _*_
__author__ = "hudingjing"
__date__ = '2019/3/27 10:40 '

from django import forms
from captcha.fields import CaptchaField

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
