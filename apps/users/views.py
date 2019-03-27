# encoding: utf-8
from django.shortcuts import render
from django.contrib.auth import authenticate,login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from .models import UserProfile
from .forms import LoginForm

class CustomerBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user=UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None

# 当我们配置url被这个view处理时，自动传入request对象.
#类写的view，不需要做get post方法判断，人家自动判断并调用相应方法
class LoginView(View):
    def get(self,request):
        return render(request, "login.html", {})
    def post(self,request):
        # 取不到时为空，username，password为前端页面name值
        login_form=LoginForm(request.POST)#这里就为form表单做了校验，并且往实例对象中添加了很多有用的校验信息
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            #如果认证信息有效，会返回一个  User  对象。authenticate()会在User 对象上设置一个属性标识那种认证后端认证了该用户
            user =authenticate(username=user_name,password=pass_word)
            if user is not None:
                #login接受一个HttpRequest对象，以及一个认证了的User对象
                #使用django的session框架给某个已认证的用户附加上session id等信息。
                login(request,user)
                return render(request,'index.html')
            else:
                return render(request, "login.html", {'msg':"用户名或密码错误"})
        else:
            return render(request, "login.html", {'form_errors': login_form})



