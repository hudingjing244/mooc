# _*_ coding: utf-8 _*_
__author__ = "hudingjing"
__date__ = '2019/3/29 16:28 '

from django.conf.urls import url
from organization.views import OrgView,UserAskView,OrgHome,OrgCourse,OrgTeacher,OrgDesc,FavorView,TeacherListView

urlpatterns = [
    # 课程机构列表url
    url(r'^list/$', OrgView.as_view(), name="org_list"),
    #课程咨询
    url(r'^add_ask/$',UserAskView.as_view(),name='add_ask'),
    # 讲师
    url(r'^teacher/list/$', TeacherListView.as_view(), name="teacher_list"),
    #课程详情页
    url(r'^home/(?P<org_id>\d+)/$',OrgHome.as_view(),name='org_home'),
    url(r'^course/(?P<org_id>\d+)/$', OrgCourse.as_view(), name='org_course'),
    url(r'^teacher/(?P<org_id>\d+)/$', OrgTeacher.as_view(), name='org_teacher'),
    url(r'^desc/(?P<org_id>\d+)/$', OrgDesc.as_view(), name='org_desc'),


    #用户收藏，包括机构、课程、讲师
    url(r'favor/$', FavorView.as_view(), name="favor"),

]