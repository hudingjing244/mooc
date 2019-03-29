# _*_ coding: utf-8 _*_
__author__ = "hudingjing"
__date__ = '2019/3/29 16:16 '
import re

from django import forms

from operation.models import UserAsk

#这种form的好处一是会先按数据库字段要求进行检查，避免重复代码。其次，它可以直接调用save保存至数据库
class UserAskForm(forms.ModelForm):

    #继承UserAsk的某些字段，在Meta外其实还可以定义新的字段
    class Meta:
        model=UserAsk
        fields=['name','phone','course_name']

    #即使通过了数据库字段检查，我还想对phone字段进行更严格的检查
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(phone):
            return phone
        else:
            raise forms.ValidationError(u"手机号码非法", code="phone_invalid")


