# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals
from datetime import datetime

from django.db import models

from organization.models import CourseOrg,Teacher

# Create your models here.

class Course(models.Model):
    name=models.CharField(max_length=50,verbose_name=u"课程名")
    category=models.CharField(max_length=20,verbose_name=u'课程类别',default=u'公开课')
    courseOrg=models.ForeignKey(CourseOrg,verbose_name=u"所属机构",null=True,blank=True)
    teacher=models.ForeignKey(Teacher,verbose_name=u"授课讲师",null=Teacher,blank=True)
    desc=models.CharField(max_length=300,verbose_name=u"课程描述")
    detail=models.TextField(verbose_name=u"课程详情")
    degree=models.CharField(verbose_name=u"课程难度",choices=(("cj","初级"),("zj","中级"),("gj","高级")),max_length=2)
    learn_time=models.IntegerField(default=0,verbose_name=u"学习时长（分钟）")
    student_nums=models.IntegerField(default=0,verbose_name=u"学习人数")
    favor_nums=models.IntegerField(default=0,verbose_name=u"收藏人数")
    image=models.ImageField(upload_to="course/%Y/%m",verbose_name=u"封面",max_length=100)
    click_nums=models.IntegerField(default=0,verbose_name=u'点击数')
    tag=models.CharField(default='',max_length=10,verbose_name=u"课程标签")
    need_known=models.CharField(max_length=300,verbose_name=u"课程须知",default='')
    teacher_tell=models.CharField(max_length=300,verbose_name=u"老师告诉你",default='')

    add_time=models.DateTimeField(default=datetime.now,verbose_name=u"添加时间")

    def get_chapter_nums(self):
        return self.lesson_set.all().count()
    def get_students(self):
        return self.usercourse_set.all()[:5]
    def get_chapter(self):
        return self.lesson_set.all()

    class Meta:
        verbose_name=u"课程"
        verbose_name_plural=verbose_name

    def __unicode__(self):
        return self.name

class Lesson(models.Model):
    course=models.ForeignKey(Course,verbose_name=u"课程")
    name=models.CharField(max_length=100,verbose_name=u"章节")
    add_time=models.DateTimeField(default=datetime.now,verbose_name=u"添加时间")

    def get_videos(self):
        return self.video_set.all()

    class Meta:
        verbose_name=u"章节"
        verbose_name_plural=verbose_name

    def __unicode__(self):
        return self.name


class Video(models.Model):
    lesson=models.ForeignKey(Lesson,verbose_name=u"章节")
    name=models.CharField(max_length=100,verbose_name=u"视频")
    learn_time=models.IntegerField(default=0,verbose_name=u"学习时长（分钟）")
    url=models.CharField(max_length=200,verbose_name=u"视频地址",blank=True,null=True)
    add_time=models.DateTimeField(default=datetime.now,verbose_name=u"添加时间")

    class Meta:
        verbose_name=u"视频"
        verbose_name_plural=verbose_name

    def __unicode__(self):
        return self.name


class CourseResourse(models.Model):
    course=models.ForeignKey(Course,verbose_name=u"课程")
    name=models.CharField(max_length=100,verbose_name=u"资源")
    download=models.FileField(upload_to="course/resourse/%Y/%m",verbose_name=u"资源文件",max_length=100)
    add_time=models.DateTimeField(default=datetime.now,verbose_name=u"添加时间")

    class Meta:
        verbose_name=u"课程资源"
        verbose_name_plural=verbose_name

    def __unicode__(self):
        return self.name