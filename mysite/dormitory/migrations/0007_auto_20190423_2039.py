# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-04-23 12:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dormitory', '0006_auto_20190423_2014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='sno',
            field=models.CharField(max_length=20, unique=True, verbose_name='学号'),
        ),
    ]
