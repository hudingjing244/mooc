# encoding: utf-8
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import CourseOrg,CityDict


# Create your views here.
class OrgView(View):
    """课程机构列表功能"""
    def get(self,request):
        #取出所有机构和城市，传到前端动态显示
        all_orgs=CourseOrg.objects.all()
        all_citys=CityDict.objects.all()
        city_id=request.GET.get("city","")
        category=request.GET.get("ct","")
        sortby=request.GET.get('sortby',"")
        if city_id:
            all_orgs=all_orgs.filter(city_id=int(city_id))
        if category:
            all_orgs=all_orgs.filter(category=int(category))
        if sortby=='students':
            all_orgs=all_orgs.order_by('-students')
        elif sortby=='courses':
            all_orgs=all_orgs.order_by('-course_nums')
        orgs_num=all_orgs.count()

        #对课程机构分页显示
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs,5, request=request)
        orgs = p.page(page)

        return render(request,"org-list.html",{
            'all_orgs':orgs,
            'all_citys':all_citys,
            'orgs_num':orgs_num,
            "city_id":city_id,
            "category":category,
            "sortby":sortby
        })
