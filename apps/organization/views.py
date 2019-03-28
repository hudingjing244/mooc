# encoding: utf-8
from django.shortcuts import render
from django.views.generic.base import View

from .models import CourseOrg

# Create your views here.
class OrgView(View):
    def get(self,request):
        return render(request,"org-list.html",{})
