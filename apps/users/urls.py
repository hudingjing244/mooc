# _*_ coding: utf-8 _*_
__author__ = "hudingjing"
__date__ = '2019/4/2 0:09 '

from django.conf.urls import url

from users.views import UserCenterView,UploadImageView,UpdatePwdView

urlpatterns=[
    #用户个人信息中心
    url(r"^center/$",UserCenterView.as_view(),name='center'),

    #用户个人中心修改头像
    url(r"^image/upload/$", UploadImageView.as_view(), name='image_upload'),
    # 用户个人中心修改密码
    url(r"^update/pwd/$", UpdatePwdView.as_view(), name='pwd_update'),
]