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
        user = request.POST.get("user")
        msg = request.session["code"]
        print(user)

        if code:
            if msg.lower() != code.lower():
                return render(request, 'dormitory/login.html', {"msg": "验证码有误！！"})
        else:
            return render(request, 'dormitory/login.html', {"msg": "验证码有误！！"})

        if name == "":
            return render(request, 'dormitory/login.html', {"msg": "用户名不能为空！！"})
        if password == "":
            return render(request, 'dormitory/login.html', {"msg": "密码不能为空！！"})


        try:
            # 判断用户是管理员还是学生
            if user == "admin":

                admin = models.Admin.objects.get(account=name)
                # 密码加密
                password = utils.pwd_by_hmac(password)
                if password == admin.password:
                    # 登录成功
                    # 通过session存储对象必须序列化,修改配置文件
                    request.session["Admin"] = admin
                    return redirect('/dormitory/index', {"msg":"登录成功"})
                else:
                    print("登录失败")
                    return render(request, 'dormitory/index.html', {"msg": "密码错误！！"})
            else:
                student = models.Student.get(son=name)
                # 密码加密
                password = utils.pwd_by_hmac(password)
                if password == student.password:
                    # 登录成功
                    # 通过session存储对象必须序列化,修改配置文件
                    request.session["Admin"] = student
                    return redirect('/dormitory/index', {"msg": "登录成功"})
                else:
                    print("登录失败")
                    return render(request, 'dormitory/index.html', {"msg": "密码错误！！"})

        except Exception as e:
            print("登录出错：", e)

            return render(request, 'dormitory/login.html', {"msg": "该用户不存在！！"})


def logout(request):
    # 退出登录
    try:
        del request.session["Admin"]

        return redirect('/dormitory/login/')
    except:
        return redirect('/dormitory/login/')


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


def add_admin(request):
    if request.method == "GET":

        return render(request, 'dormitory/add_admin.html')
    else:
        account = request.POST["account"].strip()
        password = request.POST.get("password").strip()
        name = request.POST["name"].strip()
        flag = request.POST["flag"].strip()

        try:
            models.Admin.objects.get(account=account)
            return render(request, 'dormitory/login.html', {"msg": "该用户名已存在，请重新注册！！"})

        except Exception as e:
            try:
                # 通过hmac加密密码
                password = utils.pwd_by_hmac(password)
                user = models.Admin(account=account, password=password, name=name, flag=flag)
                user.save()

                return render(request, 'dormitory/add_admin.html', {"msg": "添加成功"})

            except Exception as e:
                print("注册失败", e)
                return render(request, 'dormitory/add_admin.html', {"msg": "添加失败"})


def del_admin(request, a_id):
    try:
        admin = models.Admin.objects.get(id=a_id)
        admin.delete()
        return redirect(reverse('dormitory:admin_list'))
    except Exception as e:
        print("删除管理员失败！", e)
        return redirect(reverse('dormitory:admin_list'))


# def edit_admin(request, a_id):
#     admin = models.Admin.objects.get(id=a_id)
#     if request.method == "GET":
#
#         return render(request, "dormitory/edit_admin.html", {"admin": admin})
#     else:
#         old_password = request.POST["old_password"].strip()
#         new_password1 = request.POST["new_password1"].strip()
#         new_password2 = request.POST["new_password2"].strip()
#         name = request.POST["name"].strip()
#         flag = request.POST["flag"]
#
#         if new_password1 == new_password2:
#             if old_password != new_password1:
#
#                 old_password = utils.pwd_by_hmac(old_password)
#                 if admin.password == old_password:
#                     new_password1 = utils.pwd_by_hmac(new_password1)
#                     try:
#                         admin.password = new_password1
#                         admin.name =name
#                         admin.flag =flag
#                         admin.save()
#                         print("修改管理员信息成功。")
#                         # return redirect(reverse('dormitory:edit_admin', kwargs={"a_id": a_id}))
#                         return render(request, "dormitory/admin_list.html", {"msg": "修改成功。"})
#                     except Exception as e:
#                         print("修改保存失败", e)
#                         # return render(request, "dormitory/edit_admin.html",  {"error4": "网络异常，修改失败！请重试。"})
#
#                 else:
#                     print("3")
#                     return redirect(reverse('dormitory:edit_admin', kwargs={"a_id": a_id, "error1": "原密码输入错误！！"}))
#                     # return render(request, "/dormitory/edit_admin/{}".format(a_id), {"error3": "原密码输入错误！！！"})
#
#             else:
#                 print("2")
#                 return redirect(reverse('dormitory:edit_admin', kwargs={"a_id": a_id,"error1": "新密码不能和旧密码一样！！"}))
#                 # return render(request, "/dormitory/edit_admin/{}/".format(a_id), {"error2": "新密码不能和旧密码一样！！"})
#
#         else:
#             print("1")
#             return redirect(reverse('dormitory:edit_admin', kwargs={"a_id": a_id,"error1": "两次密码不一致！！"}))
#             # return render(request, "/dormitory/edit_admin/{}/".format(a_id), {"error1": "两次密码不一致！！"})


def reset_admin(request, a_id):
    admin = models.Admin.objects.get(id=a_id)
    password = "123456"
    password = utils.pwd_by_hashlib(password)
    admin.password = password
    admin.save()
    print("1")

    # return redirect(reverse('dormitory:admin_list', {"msg": "重置成功！"}))
    admins = models.Admin.objects.all()
    return render(request, 'dormitory/admin_list.html', {"admins": admins, "msg":"重置成功!"})



def admin_list(request):
    admins = models.Admin.objects.all()
    return render(request, 'dormitory/admin_list.html', {"admins": admins})




def add_student(request):
    pass


def del_student(request):
    pass


# 添加系别
def add_dep(request):
    if request.method == "GET":
        deps = models.Department.objects.all()
        return render(request, "dormitory/add_dep.html", {"deps": deps})
    else:
        dep_name = request.POST["dep_name"].strip()

        try:
            dep = models.Department(dep_name=dep_name)
            dep.save()
            deps = models.Department.objects.all()
            return render(request, "dormitory/add_dep.html", {"msg": "添加成功！", "deps": deps})
        except Exception as e:

            return render(request, "dormitory/add_dep.html", {"error": "该学院已存在，请重新添加！！"})


def dep_list(request):
    # 显示所有学院，并操作
    if request.method == "GET":
        deps = models.Department.objects.all()
        return render(request, "dormitory/dep_list.html", {"deps": deps})
    else:
        pass

def del_dep(request, d_id):
    try:
        dep = models.Department.objects.get(id=d_id)
        dep.delete()
        return redirect(reverse('dormitory:dep_list'), {"msg": "删除成功"})
    except Exception as e:
        print("删除学院失败！", e)
        return redirect(reverse('dormitory:dep_list', {"msg": "删除失败！！"}))



# 添加专业
def add_domain(request):
    if request.method == "GET":
        deps = models.Department.objects.all()
        # domain = models.Domain.objects.all()
        return render(request, "dormitory/add_domain.html", {"deps": deps})
    else:
        dep_name = request.POST["dep_name"].strip()

        try:
            dep = models.Department(dep_name=dep_name)
            dep.save()
            deps = models.Department.objects.all()
            return render(request, "dormitory/add_domain.html", {"msg": "添加成功！", "deps": deps})
        except Exception as e:

            return render(request, "dormitory/add_domain.html", {"error": "该专业已存在，请重新添加！！"})


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
    if request.method == "GET":
        return render(request, 'dormitory/add_notice.html')

    else:
        title = request.POST["title"].strip()
        content = request.POST["content"].strip()

        if title == "":
            return render(request, 'blog/write_article.html', {"msg_title": "标题不能为空!!!"})
        if len(title) > 150:
            return render(request, 'blog/write_article.html', {"msg_title": "标题太长!!"})
        if content == "":
            return render(request, 'blog/write_article.html', {"content_msg": "内容不能为空!!!"})

        # 文章摘要提取函数工具
        # abstract = utils.abstract(content)

        notice = models.Notice(title=title, content=content)

        try:
            notice.save()

            # 重新将缓存更新,并更新session中 articles的值
            # articles = cache_util.get_all_article(is_change=True)
            # request.session["articles"] = articles

            return render(request, 'dormitory/add_notice.html',{"msg": "文章添加成功！"} )

        except:
            return render(request, 'dormitory/add_notice.html', {"msg": "文章添加失败！！"})



def notice_list(request):
    # 显示公告列表
    notices = models.Notice.objects.all()

    return render(request, 'dormitory/notice_list.html', {"notices": notices})


def show_notice(request, n_id):
    # 显示公告内容
    try:
        notice = models.Notice.objects.get(id=n_id)

        return render(request, 'dormitory/show_notice.html', {"notice": notice})
    except Exception as e:
        print("出错了", e)
        return redirect(reverse("dormitory:notice_list"))


def edit_notice(request, n_id):
    notice = models.Notice.objects.get(id=n_id)
    if request.method == "GET":

        return render(request, 'dormitory/edit_notice.html', {"notice": notice})
    else:
        title = request.POST["title"].strip()
        content = request.POST["content"].strip()

        if title == "":
            return render(request, 'blog/edit_notice.html', {"msg_title": "标题不能为空!!!"})
        if len(title) > 150:
            return render(request, 'blog/edit_notice.html', {"msg_title": "标题太长!!"})
        if content == "":
            return render(request, 'blog/edit_notice.html', {"content_msg": "内容不能为空!!!"})

        # 文章摘要提取函数工具
        # abstract = utils.abstract(content)

        try:
            notice.title = title
            notice.content =content
            notice.save()

            # 重新将缓存更新,并更新session中 articles的值
            # articles = cache_util.get_all_article(is_change=True)
            # request.session["articles"] = articles

            return redirect(reverse('dormitory:notice_list'))

        except:
            return render(request, 'dormitory/edit_notice.html', {"msg": "文章修改失败！！"})



def del_notice(request, n_id):

    try:
        notice = models.Notice.objects.get(id=n_id)
        notice.delete()
        return redirect(reverse('dormitory:notice_list'))

    except Exception as e:

        return redirect(reverse('dormitory:notice_list'))



# 添加意见信息
def add_suggest(request):
    pass


def del_suggest(request):
    pass
