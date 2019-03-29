# _*_ coding: utf-8 _*_
__author__ = "hudingjing"
__date__ = '2019/3/29 16:28 '

from django.conf.urls import url
from organization.views import OrgView,UserAskView

urlpatterns = [
    # 课程机构列表url
    url('list/$', OrgView.as_view(), name="org_list"),
    url('add_ask/$',UserAskView.as_view(),name='add_ask'),
]