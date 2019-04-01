# encoding: utf-8
from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


from .models import Course,CourseResourse
from utils.minin_utils import LoginRequiredMinin
from operation.models import UserFavorite,CourseComment,UserCourse
# Create your views here.

class CourseListView(View):
    def get(self,request):
        all_courses=Course.objects.all().order_by('-add_time')#默认按时间排序
        hot_courses=all_courses.order_by('-click_nums')[:3]
        #全局课程搜索
        search_keywords=request.GET.get('keywords','')
        if search_keywords:
            all_courses=all_courses.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords)|Q(detail__icontains=search_keywords))#i 不区分大小写
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


class CourseInfoView(LoginRequiredMinin,View):
    """课程目录"""
    def get(self,request,course_id):
        course=Course.objects.get(id=int(course_id))

        #将学生和课程关联起来
        user_courses=UserCourse.objects.filter(user=request.user,course=course)
        if not user_courses:
            user_course=UserCourse(user=request.user,course=course)
            user_course.save()

        #学过改课的学生学过的其他课程
        user_courses=UserCourse.objects.filter(course=course)
        user_ids=[user_course.user.id for user_course in user_courses]
        all_user_courses=UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [all_user_course.course_id for all_user_course in all_user_courses]
        relate_courses=Course.objects.filter(id__in=course_ids).exclude(id=course_id).order_by('-click_nums')[:5]

        #额外资源
        all_resourses=CourseResourse.objects.filter(course=course_id)

        return render(request,'course-video.html',{
            'course':course,
            'all_resourses':all_resourses,
            'relate_courses':relate_courses
        })

class CourseCommentView(LoginRequiredMinin,View):#主要继承顺序
    """课程评论"""
    def get(self,request,course_id):
        course=Course.objects.get(id=int(course_id))
        #学过改课的学生学过的其他课程
        user_courses=UserCourse.objects.filter(course=course)
        user_ids=[user_course.user.id for user_course in user_courses]
        all_user_courses=UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [all_user_course.course_id for all_user_course in all_user_courses]
        relate_courses=Course.objects.filter(id__in=course_ids).exclude(id=course_id).order_by('-click_nums')[:5]

        all_resourses=CourseResourse.objects.filter(course=int(course_id))
        all_comments=CourseComment.objects.filter(course=int(course_id))
        return render(request,'course-comment.html',{
            'course':course,
            'all_resourses':all_resourses,
            'all_comments':all_comments,
            'relate_courses': relate_courses
        })

class AddCommentView(View):
    def post(self,request):
        if not request.user.is_authenticated:
            #用户未登录时返回给前台ajax的json数据
            return HttpResponse(
                "{'status': 'fail', 'msg':'用户未登录'}",
                content_type='application/json')
        course_id=request.POST.get('course_id','0')
        comment=request.POST.get('comments','')
        if course_id>'0' and comment:
            course_comment=CourseComment(course=Course.objects.get(id=int(course_id)),comments=comment,user=request.user)
            course_comment.save()
            return HttpResponse(
                "{'status': 'success', 'msg':'评论成功'}",
                content_type='application/json')
        else:
            return HttpResponse(
                "{'status': 'fail', 'msg':'评论失败'}",
                content_type='application/json')