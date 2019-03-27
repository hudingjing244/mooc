# _*_ coding: utf-8 _*_
__author__ = "hudingjing"
__date__ = '2019/3/27 13:59 '

from users.models import EmailVerifyRecord

def send_register_email(email,type=0):
    email_record=EmailVerifyRecord()
