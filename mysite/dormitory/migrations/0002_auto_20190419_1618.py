# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-04-19 08:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dormitory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='flag',
            field=models.IntegerField(default='1', max_length=10, verbose_name='权限标识符'),
        ),
        migrations.AlterField(
            model_name='admin',
            name='name',
            field=models.CharField(max_length=100, null=True, unique=True, verbose_name='姓名'),
        ),
    ]
