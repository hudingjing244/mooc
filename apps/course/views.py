# encoding: utf-8
from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


from .models import Course
# Create your views here.

class CourseListView(View):
    def get(self,request):
        all_courses=Course.objects.all().order_by('-add_time')#默认按时间排序
        hot_courses=all_courses.order_by('-click_nums')[:3]
        #课程排序
        sortby = request.GET.get('sortby', "")
        if sortby == 'student_nums':
            all_orgs = all_courses.order_by('-student_nums')
        elif sortby == 'hot':
            all_orgs = all_courses.order_by('-click_nums')
        # 对课程分页显示,注意字典参数得替换成每页的数据，以及模板中的quryset加上.object_list
        #页码不合法时 显示第一页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 6, request=request)
        courses = p.page(page)

        return render(request,'course-list.html',{
            'all_courses':courses,
            "sortby":sortby,
            'hot_courses':hot_courses
        })