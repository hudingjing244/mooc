# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2019-03-29 20:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0003_auto_20190329_1437'),
        ('course', '0002_auto_20190325_1626'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='courseOrg',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.CourseOrg', verbose_name='\u6240\u5c5e\u673a\u6784'),
        ),
    ]