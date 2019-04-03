# _*_ coding: utf-8 _*_
__author__ = "hudingjing"
__date__ = '2019/4/2 0:09 '

from django.conf.urls import url

from users.views import UserCenterView,UploadImageView,UpdatePwdView,SendEmailVerifyCodeView,ChangeEmailView,MyCourseView

urlpatterns=[
    #用户个人信息中心
    url(r"^info/$",UserCenterView.as_view(),name='center'),

    #用户个人中心修改头像
    url(r"^image/upload/$", UploadImageView.as_view(), name='image_upload'),
    # 用户个人中心修改密码
    url(r"^update/pwd/$", UpdatePwdView.as_view(), name='pwd_update'),
    # 用户个人中心发送邮箱验证码
    url(r"^sendemail_code/$", SendEmailVerifyCodeView.as_view(), name='send_email_verifyCode'),
    # 用户个人中心修改邮箱
    url(r"^update_email/$", ChangeEmailView.as_view(), name='change_email'),
    # 用户个人中心我的课程
    url(r"^mycourse/$", MyCourseView.as_view(), name='mycourse'),
]