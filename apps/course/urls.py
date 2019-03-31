# _*_ coding: utf-8 _*_
__author__ = "hudingjing"
__date__ = '2019/3/31 17:13 '

from django.conf.urls import url
from course.views import CourseListView

urlpatterns = [
    #课程列表页
    url(r'^list/', CourseListView.as_view(),name='course_list'),
    ]