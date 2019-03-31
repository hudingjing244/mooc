# encoding: utf-8
from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


from .models import Course
from operation.models import UserFavorite
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

class CourseDetailView(View):
    """
    课程详情页
    """
    def get(self,request,course_id):
        course=Course.objects.get(id=int(course_id))
        course.click_nums+=1
        course.save()

        has_favor_course=False
        has_favor_org=False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user,fav_id=course.id,fav_type=1):
                has_favor_course=True
            if UserFavorite.objects.filter(user=request.user,fav_id=course.courseOrg.id,fav_type=2):
                has_favor_org=True


        tag=course.tag
        if tag:
            related_courses=Course.objects.filter(tag=tag).exclude(id=int(course_id))[:3]
        else:
            related_courses=[]
        return render(request,'course-detail.html',{
            'course':course,
            'related_courses':related_courses,
            'has_favor_course':has_favor_course,
            'has_favor_org':has_favor_org,
        })