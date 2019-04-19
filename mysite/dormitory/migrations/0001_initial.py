# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-04-19 00:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='管理员编号')),
                ('account', models.CharField(max_length=100, unique=True, verbose_name='登录名')),
                ('password', models.CharField(max_length=100, verbose_name='密码')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='姓名')),
                ('flag', models.IntegerField(max_length=10, verbose_name='权限标识符')),
            ],
        ),
        migrations.CreateModel(
            name='Charge',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='水电主键')),
                ('month', models.DateField(auto_now=True, verbose_name='月份')),
                ('category', models.CharField(default='电费', max_length=20, verbose_name='类别')),
                ('money', models.FloatField(max_length=20, verbose_name='金额')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='系别主键')),
                ('dep_name', models.CharField(max_length=100, unique=True, verbose_name='系别名称')),
            ],
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='专业主键')),
                ('dom_name', models.CharField(max_length=100, unique=True, verbose_name='专业名称')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dormitory.Department', verbose_name='系别名称')),
            ],
        ),
        migrations.CreateModel(
            name='Dorm',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='宿舍主键')),
                ('suno', models.CharField(max_length=50, unique=True, verbose_name='宿舍编号')),
                ('max_num', models.IntegerField(default=8, verbose_name='床铺数量')),
                ('people', models.IntegerField(default=0, verbose_name='已住人数')),
                ('sex', models.CharField(default='男', max_length=50, verbose_name='宿舍性别')),
            ],
        ),
        migrations.CreateModel(
            name='Floor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='楼层主键')),
                ('con', models.CharField(max_length=20, unique=True, verbose_name='楼层编号')),
                ('sex', models.CharField(default='男', max_length=50, verbose_name='宿舍性别')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dormitory.Department', verbose_name='所属系别')),
                ('domain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dormitory.Domain', verbose_name='所属专业')),
            ],
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='编号')),
                ('title', models.CharField(max_length=200, verbose_name='标题')),
                ('content', models.TextField(verbose_name='内容')),
                ('publishTime', models.DateTimeField(auto_now_add=True, verbose_name='发表时间')),
                ('count', models.IntegerField(default=0, verbose_name='点击量')),
            ],
        ),
        migrations.CreateModel(
            name='Repairs',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='宿舍主键')),
                ('content', models.TextField(max_length=500, verbose_name='报修内容')),
                ('date_time', models.DateField(auto_now_add=True, verbose_name='报修时间')),
                ('flag', models.CharField(default='待维修', max_length=50, verbose_name='维修状态')),
                ('dorm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dormitory.Dorm', verbose_name='宿舍编号')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='学生主键')),
                ('sno', models.IntegerField(max_length=12, unique=True, verbose_name='学号')),
                ('password', models.CharField(max_length=100, verbose_name='密码')),
                ('name', models.CharField(max_length=100, verbose_name='姓名')),
                ('gender', models.CharField(max_length=20, verbose_name='性别')),
                ('age', models.IntegerField(default=18, verbose_name='年龄')),
                ('avatar', models.CharField(default='/static/blog/img/avatar08.jpg', max_length=255, verbose_name='头像')),
                ('tel', models.IntegerField(max_length=50, verbose_name='电话号码')),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dormitory.Department', verbose_name='所属系别')),
                ('domain', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dormitory.Domain', verbose_name='所属专业')),
                ('dorm', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dormitory.Dorm', verbose_name='宿舍编号')),
                ('floor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dormitory.Floor', verbose_name='所属楼层')),
            ],
        ),
        migrations.CreateModel(
            name='Suggest',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='意见主键')),
                ('content', models.TextField(max_length=500, verbose_name='意见内容')),
                ('date_time', models.DateField(auto_now_add=True, verbose_name='提交时间')),
                ('reply', models.CharField(max_length=200, null=True, verbose_name='回复')),
                ('dorm', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dormitory.Dorm', verbose_name='宿舍编号')),
                ('sno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dormitory.Student', verbose_name='学号')),
            ],
        ),
        migrations.CreateModel(
            name='Tower',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='楼房主键')),
                ('num', models.CharField(max_length=20, unique=True, verbose_name='楼房编号')),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='tower',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dormitory.Tower', verbose_name='所属楼房'),
        ),
        migrations.AddField(
            model_name='floor',
            name='tower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dormitory.Tower', verbose_name='所属楼房'),
        ),
        migrations.AddField(
            model_name='dorm',
            name='floor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dormitory.Floor', verbose_name='所属楼层'),
        ),
        migrations.AddField(
            model_name='dorm',
            name='tower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dormitory.Tower', verbose_name='所属楼房'),
        ),
        migrations.AddField(
            model_name='charge',
            name='dorm',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dormitory.Dorm', verbose_name='宿舍编号'),
        ),
    ]
