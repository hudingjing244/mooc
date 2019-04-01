# _*_ coding: utf-8 _*_
__author__ = "hudingjing"
__date__ = '2019/4/1 14:14 '

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredMinin(object):
    """用户登录状态检查，不通过则跳转到登录页面"""
    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self,request,*args,**kwargs):
        return super(LoginRequiredMinin, self).dispatch(request,*args,**kwargs)