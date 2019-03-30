# _*_ coding: utf-8 _*_
__author__ = "hudingjing"
__date__ = '2019/3/29 16:28 '

from django.conf.urls import url
from organization.views import OrgView,UserAskView,OrgHome,OrgCourse,OrgTeacher,OrgDesc

urlpatterns = [
    # 课程机构列表url
    url(r'list/$', OrgView.as_view(), name="org_list"),
    url(r'add_ask/$',UserAskView.as_view(),name='add_ask'),
    url(r'home/(?P<org_id>\d+)/$',OrgHome.as_view(),name='org_home'),
    url(r'course/(?P<org_id>\d+)/$', OrgCourse.as_view(), name='org_course'),
    url(r'teacher/(?P<org_id>\d+)/$', OrgTeacher.as_view(), name='org_teacher'),
    url(r'desc/(?P<org_id>\d+)/$', OrgDesc.as_view(), name='org_desc'),

]