# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2019-03-31 20:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0004_course_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='category',
            field=models.CharField(default='\u516c\u5f00\u8bfe', max_length=20, verbose_name='\u8bfe\u7a0b\u7c7b\u522b'),
        ),
    ]
