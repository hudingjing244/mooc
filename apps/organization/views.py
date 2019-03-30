# encoding: utf-8
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse

from .models import CourseOrg, CityDict
from .forms import UserAskForm


# Create your views here.
class OrgView(View):
    """课程机构列表功能"""

    def get(self, request):
        # 取出所有机构和城市，传到前端动态显示
        all_orgs = CourseOrg.objects.all()
        all_citys = CityDict.objects.all()
        city_id = request.GET.get("city", "")
        category = request.GET.get("ct", "")
        sortby = request.GET.get('sortby', "")
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))
        if category:
            all_orgs = all_orgs.filter(category=int(category))
        if sortby == 'students':
            all_orgs = all_orgs.order_by('-students')
        elif sortby == 'courses':
            all_orgs = all_orgs.order_by('-course_nums')
        orgs_num = all_orgs.count()

        # 对课程机构分页显示
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, 5, request=request)
        orgs = p.page(page)

        return render(request, "org-list.html", {
            'all_orgs': orgs,
            'all_citys': all_citys,
            'orgs_num': orgs_num,
            "city_id": city_id,
            "category": category,
            "sortby": sortby
        })


class UserAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            # 如果表单数据合法，保存至数据库并返回相应的记录对象
            user_ask = userask_form.save(commit=True)
            # 并且回传AJAX所需要的json数据，用于刷新页面
            return HttpResponse(
                "{'status':'success'}",
                content_type="application/json")
        else:
            return HttpResponse(
                "{'status': 'fail', 'msg':'添加出错'}",
                content_type='application/json')


class OrgHome(View):
    """课程机构主页"""

    def get(self, request, org_id):
        org = CourseOrg.objects.get(id=int(org_id))
        all_courses = org.course_set.all()[:4]
        all_teachers = org.teacher_set.all()[:3]
        current_page='home'
        return render(request, 'org-detail-homepage.html', {
            "all_courses": all_courses,
            "all_teachers": all_teachers,
            'org':org,
            'current_page':current_page
        })


class OrgCourse(View):
    """课程机构课程列表页"""

    def get(self, request, org_id):
        org = CourseOrg.objects.get(id=int(org_id))
        all_courses = org.course_set.all()[:4]
        current_page = 'course'

        return render(request, 'org-detail-course.html', {
            "all_courses": all_courses,
            'org': org,
            'current_page': current_page

        })


class OrgTeacher(View):
    """课程机构讲师列表页"""

    def get(self, request, org_id):
        org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = org.teacher_set.all()[:3]
        current_page = 'teacher'

        return render(request, 'org-detail-teachers.html', {
            "all_teachers": all_teachers,
            'org': org,
            'current_page': current_page

        })


class OrgDesc(View):
    """课程机构介绍页"""

    def get(self, request, org_id):
        org = CourseOrg.objects.get(id=int(org_id))
        current_page = 'desc'

        return render(request, 'org-detail-desc.html', {
            'org': org,
            'current_page': current_page

        })
