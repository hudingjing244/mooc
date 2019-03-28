# _*_ coding: utf-8 _*_
__author__ = "hudingjing"
__date__ = '2019/3/27 13:59 '

from random import Random

# 导入Django自带的邮件模块
from django.core.mail import send_mail
# 导入setting中发送邮件的配置
from mooc.settings import EMAIL_FROM

from users.models import EmailVerifyRecord


def generate_random_code(random_lenth=8):
    str = ''
    chars = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm0123456789'
    length = len(chars) - 1
    ran = Random()
    for i in range(random_lenth):
        str += chars[ran.randint(0, length)]  # [0,length],左右都是闭区间
    return str


def send_register_email(email, send_type='register'):
    # 先在数据库存储一条邮件验证的记录，用于用户点击链接后进行验证
    random_code = generate_random_code(16)
    email_record = EmailVerifyRecord()
    email_record.email = email
    email_record.verify_code = random_code
    email_record.send_type = send_type
    email_record.save()

    # 定义邮件标题，内容，收发人等
    email_subject = ''
    email_body = ''
    if send_type == 'register':
        email_subject = '天才靖MOOC网用户注册激活链接'
        # 需要动态生成一个active/目录
        email_body = '请点击链接以激活您的账号：http://127.0.0.1:8000/active/{0}'.format(
            random_code)
    elif send_type == 'forget':
        email_subject = '天才靖MOOC网用户密码重置链接'
        # 需要动态生成一个active/目录
        email_body = '请点击链接以重置您的密码：http://127.0.0.1:8000/reset_pwd/{0}'.format(
            random_code)

    # 发送邮件
    send_status = send_mail(email_subject, email_body, EMAIL_FROM, [email])
    if send_status:
        pass
