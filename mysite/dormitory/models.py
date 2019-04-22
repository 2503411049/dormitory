from django.db import models


# 定义用户类，在Django中，定义model需要继承models.Model类

# 定义系别类
class Department(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="系别主键")
    dep_name = models.CharField(max_length=100, unique=True, verbose_name="系别名称")


# 定义专业
class Domain(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="专业主键")
    dom_name = models.CharField(max_length=100, unique=True, verbose_name="专业名称")
    # 设置外键 外键为系别id
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="系别名称")


# 定义楼房
class Tower(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="楼房主键")
    num = models.CharField(max_length=20, unique=True, verbose_name="楼房编号")


# 定义楼层
class Floor(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="楼层主键")
    con = models.CharField(max_length=20, unique=True, verbose_name="楼层编号")
    sex = models.CharField(max_length=50, default="男", verbose_name="宿舍性别")
    # 外键
    tower = models.ForeignKey(Tower, on_delete=models.CASCADE, verbose_name="所属楼房")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="所属系别")
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, verbose_name="所属专业")


# 定义宿舍
class Dorm(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="宿舍主键")
    suno = models.CharField(max_length=50, unique=True, verbose_name="宿舍编号")
    # 外键
    tower = models.ForeignKey(Tower, on_delete=models.CASCADE, verbose_name="所属楼房")
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, verbose_name="所属楼层")

    max_num = models.IntegerField(default=8,  verbose_name="床铺数量")
    people = models.IntegerField(default=0,  verbose_name="已住人数")
    sex = models.CharField(max_length=50, default="男", verbose_name="宿舍性别")


# 定义报修
class Repairs(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="宿舍主键")
    # 外键
    dorm = models.ForeignKey(Dorm, on_delete=models.CASCADE, verbose_name="宿舍编号")
    content = models.TextField(max_length=500, verbose_name="报修内容")
    date_time = models.DateField(auto_now_add=True, verbose_name="报修时间")
    flag = models.CharField(max_length=50, default="待维修", verbose_name="维修状态")


# 定义水电
class Charge(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="水电主键")
    # 外键
    dorm = models.ForeignKey(Dorm, on_delete=models.CASCADE, verbose_name="宿舍编号")
    month = models.DateField(auto_now=True, verbose_name="月份")
    category = models.CharField(max_length=20, default="电费", verbose_name="类别")
    money = models.FloatField(max_length=20, verbose_name="金额")


# 定义学生
class Student(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="学生主键")
    sno = models.IntegerField( unique=True, verbose_name="学号")
    password = models.CharField(max_length=100, verbose_name="密码")
    name = models.CharField(max_length=100, verbose_name="姓名")
    gender = models.CharField(max_length=20, verbose_name="性别")
    age = models.IntegerField( verbose_name="年龄")
    avatar = models.CharField(max_length=255, default='/static/blog/img/avatar08.jpg', verbose_name="头像")
    # 外键
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, verbose_name="所属系别")
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, null=True, verbose_name="所属专业")

    tel = models.IntegerField( verbose_name="电话号码")
    tower = models.ForeignKey(Tower, on_delete=models.CASCADE, null=True, verbose_name="所属楼房")
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, null=True, verbose_name="所属楼层")
    dorm = models.ForeignKey(Dorm, on_delete=models.CASCADE, null=True, verbose_name="宿舍编号")


# 定义意见
class Suggest(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="意见主键")
    dorm = models.ForeignKey(Dorm, on_delete=models.CASCADE, null=True, verbose_name="宿舍编号")
    sno = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="学号")
    content = models.TextField(max_length=500, verbose_name="意见内容")
    date_time = models.DateField(auto_now_add=True, verbose_name="提交时间")
    reply = models.CharField(max_length=200, null=True, verbose_name="回复")


# 定义管理员
class Admin(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="管理员编号")
    account = models.CharField(max_length=100, unique=True, verbose_name="登录名")
    password = models.CharField(max_length=100, verbose_name="密码")
    name = models.CharField(max_length=100, null=True, unique=True, verbose_name="姓名")
    flag = models.CharField( default="1", max_length=10, verbose_name="权限标识符")


# 定义公告
class Notice(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="编号")
    title = models.CharField(max_length=200, verbose_name="标题")
    content = models.TextField(verbose_name="内容")
    publishTime = models.DateTimeField(auto_now_add=True, verbose_name="发表时间")
    count = models.IntegerField(default=0, verbose_name="点击量")
