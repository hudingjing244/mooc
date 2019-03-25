# _*_ coding: utf-8 _*_
__author__ = "hudingjing"
__date__ = '2019/3/25 16:11 '

import xadmin
from xadmin import views

from .models import EmailVerifyRecord, UserProfile, Banner

class BaseSetting(object):
    # 开启主题功能
    enable_themes = True
    use_bootswatch = True


# xadmin 全局配置参数信息设置
class GlobalSettings(object):
    site_title = "MOOC后台管理"
    site_footer = "Tigerouse Corporation"
    # 收起菜单
    menu_style = "accordion"


# 创建admin的管理类,这里不再是继承admin，而是继承object
class EmailVerifyRecordAdmin(object):
    list_display = [
        'verify_code',
        'email',
        'send_type',
        'send_time']  # 后台管理显示的字段
    # 后台提供搜索框，并且能按列表中的字段进行查询(没有选项，对全部字段进行匹配）
    search_fields = ['verify_code', 'email', 'send_type']
    list_filter = [
        'verify_code',
        'email',
        'send_type',
        'send_time']  # 后台提供过滤器，精确到字段的过滤展示


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']  # 不要按时间搜索，会出很多问题
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
# xadmin.site.register(UserProfile, UserProfileAdmin)   xadmin自动注册过了
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)