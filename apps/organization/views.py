# encoding: utf-8
from django.shortcuts import render
from django.views.generic.base import View

from .models import CourseOrg,CityDict

# Create your views here.
class OrgView(View):
    """课程机构列表功能"""
    def get(self,request):
        #取出所有机构和城市，传到前端动态显示
        all_orgs=CourseOrg.objects.all()
        all_citys=CityDict.objects.all()
        orgs_num=all_orgs.count()
        return render(request,"org-list.html",{
            'all_orgs':all_orgs,
            'all_citys':all_citys,
            'orgs_num':orgs_num
        })
