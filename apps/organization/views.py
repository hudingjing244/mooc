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
        orgs_num=all_orgs.count()
        city_id=request.GET.get("city","")
        if city_id:
            all_orgs=all_orgs.filter(city_id=int(city_id))

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
            "city_id":city_id
        })
