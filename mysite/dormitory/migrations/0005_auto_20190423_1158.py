# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-04-23 03:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dormitory', '0004_tower_sex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='floor',
            name='con',
            field=models.CharField(max_length=20, verbose_name='楼层编号'),
        ),
    ]
