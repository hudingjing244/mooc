# encoding: utf-8
import json

from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetForm, RestPwdForm, UploadImageForm,UserInfoForm
from utils.email_send import send_register_email
from utils.minin_utils import LoginRequiredMinin
from operation.models import UserCourse,UserFavorite,UserMessage
from organization.models import CourseOrg,Teacher
from course.models import Course


class CustomerBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(
                Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None

# 当我们配置url被这个view处理时，自动传入request对象.
# 类写的view，不需要做get post方法判断，人家自动判断并调用相应方法


class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        # 取不到时为空，username，password为前端页面name值
        # 这里就为form表单做了校验，并且往实例对象中添加了很多有用的校验信息
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            # 如果认证信息有效，会返回一个  User  对象。authenticate()会在User
            # 对象上设置一个属性标识那种认证后端认证了该用户
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                # login接受一个HttpRequest对象，以及一个认证了的User对象
                # 使用django的session框架给某个已认证的用户附加上session id等信息。
                if user.is_active:
                    login(request, user)
                    return render(request, 'index.html')
                else:
                    return render(request, "login.html", {'msg': "请先激活您的账户"})
            else:
                return render(request, "login.html", {'msg': "用户名或密码错误"})
        else:
            return render(request, "login.html", {'form_errors': login_form})


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(
            request, 'register.html', {
                "register_form": register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            # 合法的注册记录存至数据库
            user_email = request.POST.get("email", "")
            if UserProfile.objects.filter(email=user_email):
                return render(
                    request, 'register.html', {
                        "register_form": register_form, "msg": "该邮箱已被注册"})
            else:
                pass_word = request.POST.get("password", "")
                user_profile = UserProfile()
                user_profile.username = user_email
                user_profile.email = user_email
                user_profile.password = make_password(pass_word)
                user_profile.is_active = False
                user_profile.save()

                #发送站内注册成功信息
                user_message=UserMessage(user=user_profile.id,message="欢迎来到MOOC网，快去课程中心寻找自己心仪的课程为自己充充电吧！")

                # 邮箱激活
                send_register_email(user_email, 'register')

                return render(request, 'index.html')

        else:
            return render(
                request, 'register.html', {
                    "register_form": register_form})


class ActiveView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(verify_code=active_code)
        if all_records:
            for record in all_records:
                user = UserProfile.objects.get(email=record.email)
                user.is_active = True
                user.save()
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, "forgetpwd.html", {"forget_form": forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            send_register_email(email, "forget")
            return render(request, "send_success.html")
        else:
            return render(
                request, "forgetpwd.html", {
                    "forget_form": forget_form})


class ResetView(View):
    def get(self, request, reset_code):
        all_records = EmailVerifyRecord.objects.filter(verify_code=reset_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html", {"email": email})


class ModifyView(View):
    def post(self, request):
        reset_form = RestPwdForm(request.POST)
        if reset_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(
                    request, "password_reset.html", {
                        "email": email, "msg": "两次密码不一致，请再次确认"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()
            return render(request, "login.html")
        else:
            email = request.POST.get("email", "")
            return render(
                request, "password_reset.html", {
                    "email": email, "reset_form": reset_form})


class UserCenterView(LoginRequiredMinin, View):
    """用户中心"""

    def get(self, request):
        return render(request, 'usercenter-info.html', {})
    def post(self,request):
        # 用户个人信息修改表单，注意如果是修改，ModelForm要指定实例对象，否则会新增一个实例，那就不是修改了
        user_info_form=UserInfoForm(request.POST,instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse("{'status':'success'}",content_type="application/json")
        else:
            return HttpResponse(json.dumps(user_info_form.errors),content_type="application/json")



class UploadImageView(LoginRequiredMinin, View):
    """上传头像"""

    def post(self, request):
        image_form = UploadImageForm(
            request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse(
                "{'status':'success'}",
                content_type='application/json')
        else:
            return HttpResponse(
                "{'status':'fail'}",
                content_type='application/json')

class UpdatePwdView(LoginRequiredMinin,View):
    """
    个人中心修改密码
    """
    def post(self, request):
        reset_form = RestPwdForm(request.POST)
        if reset_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return HttpResponse(
                    "{'status':'fail','msg':'密码不一致'}",
                    content_type='application/json')
            user = request.user
            user.password = make_password(pwd1)
            user.save()
            return HttpResponse(
                "{'status':'success','msg':'密码修改成功'}",
                content_type='application/json')
        else:
            return HttpResponse(
                json.dumps(reset_form.errors),
                content_type='application/json')

class SendEmailVerifyCodeView(LoginRequiredMinin,View):
    """
    发送邮箱验证码
    """
    def get(self,request):
        email=request.GET.get('email',"")

        if UserProfile.objects.filter(email=email):
            return HttpResponse(
                "{'status':'fail','email':'该邮箱已经被注册'}",
                content_type='application/json')

        send_register_email(email,'change')

        return HttpResponse(
            "{'status':'success','email':'发送成功'}",
            content_type='application/json')

class ChangeEmailView(LoginRequiredMinin,View):
    """
    修改绑定邮箱
    """
    def post(self,requset):
        email=requset.POST.get('email','')
        code=requset.POST.get('code','')

        if EmailVerifyRecord.objects.filter(email=email,verify_code=code,send_type='change'):
            user=requset.user
            user.email=email
            user.save()
            return HttpResponse(
                "{'status':'success','email':'修改成功'}",
                content_type='application/json')
        else:
            return HttpResponse(
                "{'status':'fail','email':'验证码出错'}",
                content_type='application/json')

class MyCourseView(LoginRequiredMinin,View):
    """我的课程页面"""
    def get(self,request):
        all_courses=UserCourse.objects.filter(user=request.user)
        return render(request,"usercenter-mycourse.html",{
            'all_courses':all_courses,
        })

#写完发现，其实这几个收藏完全可以用一个url一个view处理，请求url中带上一个区分类别的参数就好了
class MyFavOrgView(LoginRequiredMinin,View):
    """我的收藏机构页面"""
    def get(self,request):
        org_list=[]
        fav_orgs=UserFavorite.objects.filter(user=request.user,fav_type=2)
        for fav_org in fav_orgs:
            org_id=fav_org.fav_id
            org_list.append(CourseOrg.objects.get(id=org_id))
        return render(request,"usercenter-fav-org.html",{
            'org_list':org_list,
        })


class MyFavTeacherView(LoginRequiredMinin,View):
    """我的收藏讲师页面"""
    def get(self,request):
        teacher_list=[]
        fav_teachers=UserFavorite.objects.filter(user=request.user,fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id=fav_teacher.fav_id
            teacher_list.append(Teacher.objects.get(id=teacher_id))
        return render(request,"usercenter-fav-teacher.html",{
            'teacher_list':teacher_list,
        })


class MyFavCourseView(LoginRequiredMinin,View):
    """我的收藏课程页面"""
    def get(self,request):
        course_list=[]
        fav_courses=UserFavorite.objects.filter(user=request.user,fav_type=1)
        for fav_course in fav_courses:
            course_id=fav_course.fav_id
            course_list.append(Course.objects.get(id=course_id))
        return render(request,"usercenter-fav-course.html",{
            'course_list':course_list,
        })


class MyMessageView(LoginRequiredMinin,View):
    """我的消息"""
    def get(self,request):
        all_message=UserMessage.objects.filter(user=request.user.id)
        # 对消息分页显示
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_message, 5, request=request)
        messages = p.page(page)

        return render(request,'usercenter-message.html',{
                    'messages':messages,
        })


