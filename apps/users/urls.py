# _*_ coding: utf-8 _*_
__author__ = "hudingjing"
__date__ = '2019/4/2 0:09 '

from django.conf.urls import url

from users.views import UserCenterView

urlpatterns=[
    url(r"^center/$",UserCenterView.as_view(),name='center')
]