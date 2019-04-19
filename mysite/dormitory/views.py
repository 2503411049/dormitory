import uuid
import logging
from datetime import datetime
from io import BytesIO

from django.shortcuts import render
# 重定向
from django.shortcuts import redirect
# 路由反解析
from django.shortcuts import reverse
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods, require_safe

from django.forms.models import model_to_dict
# 序列化器，Django用来序列化queryset对象
from django.core.serializers import serialize
# django分页
from django.core.paginator import Paginator
# 导入settings 配置
from django.conf import settings

from . import models
from .utils import require_login
from . import utils
# from . import cache_util


def index(request):

    return render(request, 'dormitory/index.html')


def code(request):
    # 验证码视图函数
    img, msg = utils.creat_code()
    # 获取一个字节IO
    file = BytesIO()
    img.save(file, "PNG")
    # 将验证码的值存储到session
    request.session["code"] = msg

    return HttpResponse(file.getvalue(), 'image/png')


def login(request):
    # 登录页面
    if request.method == "GET":
        return render(request, 'dormitory/login.html')

    elif request.method == "POST":
        name = request.POST.get("account").strip()
        password = request.POST["password"].strip()
        code = request.POST.get("code", None)

        # 数据校验
        # 第一步验证码验证
        # count = request.session.get("login_error", 0)
        # print("count--------", count)
        # if count >= 2:
        #     msg = request.session["code"]
        #     if msg.lower() != code.lower():
        #         return render(request, 'dormitory/login.html', {"msg": "验证码有误！！"})
        # else:
        #     request.COOKIES["login_error"] = 0

        # count = request.COOKIES.get("")
        if name == "":
            return render(request, 'dormitory/login.html', {"msg": "用户名不能为空！！"})
        if password == "":
            return render(request, 'dormitory/login.html', {"msg": "密码不能为空！！"})

        try:
            user = models.Admin.objects.get(account=name)
            # 密码加密
            password = utils.pwd_by_hmac(password)
            if password == user.password:
                # 登录成功
                # 通过session存储对象必须序列化
                # request.session["loginUser"] = user

                # articles = models.Article.objects.all().order_by("-count")
                # request.session["login_error"] = 0
                # 记录日志
                # logger.info("--login--" + user.name + "登录了博客" + "---" + str(datetime.now()))
                print("登录成功")
                return redirect('/dormitory/index', {"msg":"登录成功"})
            else:
                print("登录失败")
                # print(count)
                # count += 1
                # request.session["login_error"] = count
                # logger.error("--login_pwd_error--" + user.name + "尝试登录，密码错误" + "---" + str(datetime.now()))
                return render(request, 'dormitory/index.html', {"msg": "密码错误！！"})

        except Exception as e:
            print("登录出错：", e)
            # count += 1
            # print(count)
            # request.session["login_error"] = count
            # logger.warning("--login_user_error--" + name + "尝试登录，该账户不存在" + "---" + str(datetime.now()))
            return render(request, 'dormitory/login.html', {"msg": "该用户不存在！！"})


def admin_register(request):
    # 注册页面
    if request.method == "GET":

        context = {"msg": "请认真填写如下选项"}
        return render(request, 'dormitory/login.html', context)

    elif request.method == "POST":
        # 接收参数

        account = request.POST["account"].strip()
        password = request.POST.get("password").strip()
        code = request.POST.get("code")

        print(account, password, code)
        # 验证码判断

        # msg = request.session["code"]
        # if msg.lower() != code.lower():
        #     return render(request, 'dormitory/login.html', {"msg": "验证码有误！！"})
        #
        # if account.strip() == "":
        #
        #     return render(request, 'dormitory/login.html', {"msg": "用户名不能为空"})
        #
        # elif len(password.strip()) < 6:
        #     return render(request, 'dormitory/login.html', {"msg": "密码不能小于6位！！"})

        try:
            models.Admin.objects.get(account=account)
            return render(request, 'dormitory/login.html', {"msg": "该用户名已存在，请重新注册！！"})

        except Exception as e:
            try:
                # 通过hmac加密密码
                password = utils.pwd_by_hmac(password)
                user = models.Admin(account=account, password=password)
                user.save()

                # 记录日志
                # logger.info("--register_user--" + user.name + "该用户在" + str(datetime.now()) + "注册了用户")
                return render(request, 'dormitory/login.html')

            except Exception as e:
                print("注册失败", e)
                # logger.error("--register_user_error--" + name + "该用户在" + str(datetime.now()) + "注册用户失败！错误是：" + str(e))
                return render(request, 'dormitory/login.html', {"msg": "注册失败"})


def add_student(request):
    pass


def del_student(request):
    pass


# 添加系别
def add_dep(request):
    pass


def del_dep(request):
    pass


# 添加专业
def add_domain(request):
    pass


def del_domain(request):
    pass


# 添加楼房
def add_tower(request):
    pass


def del_tower(request):
    pass


# 添加楼层
def add_floor(request):
    pass


# 添加宿舍
def add_dorm(request):
    pass


def del_dorm(request):
    pass


# 添加报修管理
def add_repairs(request):
    pass


# 添加水电费管理
def add_charge(request):
    pass


def del_charge(request):
    pass


# 添加公告信息
def add_notice(request):
    pass


def del_notice(request):
    pass


# 添加意见信息
def add_suggest(request):
    pass


def del_suggest(request):
    pass
