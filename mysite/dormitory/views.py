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

    # return render(request, 'dormitory/notice_list.html')
    return redirect(reverse('dormitory:notice_list'))

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
        print("---", name, password, user)

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
                # 管理员登录
                admin = models.Admin.objects.get(account=name)
                # 密码加密
                password = utils.pwd_by_hmac(password)
                if password == admin.password:
                    # 登录成功
                    # 通过session存储对象必须序列化,修改配置文件
                    request.session["Admin"] = admin
                    # return render('/dormitory/index.html', {"msg":"登录成功"})
                    request.session["Login"] = "admin"
                    return render(request, 'dormitory/index.html', {"ID": "管理员"})
                else:
                    print("登录失败")
                    return render(request, 'dormitory/index.html', {"msg": "密码错误！！"})
            else:
                # 学生登录
                student = models.Student.objects.get(sno=name)
                # 密码加密
                password = utils.pwd_by_hmac(password)
                if password == student.password:
                    # 登录成功
                    # 通过session存储对象必须序列化,修改配置文件
                    request.session["Student"] = student
                    request.session["Login"] = "student"

                    return render(request, 'dormitory/student_base.html',{"ID": "学生"})

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
    # return redirect(reverse('dormitory:admin_list', {"msg": "重置成功！"}))
    admins = models.Admin.objects.all()
    return render(request, 'dormitory/admin_list.html', {"admins": admins, "msg":"重置成功!"})


def admin_list(request):
    admins = models.Admin.objects.all()
    return render(request, 'dormitory/admin_list.html', {"admins": admins})


def add_student(request):
    if request.method == "GET":
        deps = models.Department.objects.all()

        return render(request, 'dormitory/add_student.html', {"deps": deps})

    else:
        sno = request.POST["sno"].strip()
        password = request.POST["password"].strip()
        name = request.POST["name"].strip()
        gender = request.POST["gender"]
        department = request.POST["department"]
        domain = request.POST["domain"]

        print(sno, password, name, gender, department, domain)
        department = models.Department.objects.get(id=department)
        domain = models.Domain.objects.get(id=domain)

        if sno == "":
            return render(request, 'dormitory/add_student.html', {"error1": "提示信息：学号不能为空！"})
        if password == "":
            return render(request, 'dormitory/add_student.html', {"error1": "提示信息：密码不能为空！"})
        if name == "":
            return render(request, 'dormitory/add_student.html', {"error1": "提示信息：姓名不能为空！"})
        if domain =="":
            return render(request, 'dormitory/add_student.html', {"error1": "提示信息：专业信息不能为空！"})
        if department == "---全部---":
            return render(request, 'dormitory/add_student.html', {"error1": "提示信息：请选择学院信息！"})

        try:
            models.Student.objects.get(sno=sno)

            return render(request, 'dormitory/add_student.html', {"error1": "提示信息：该学号已存在！"})
        except:

            try:
                password = utils.pwd_by_hmac(password)
                student = models.Student(sno=sno, password=password, name=name, gender=gender, department=department, domain=domain)
                student.save()
                return render(request, 'dormitory/add_student.html', {"msg": "添加成功！"})
            except Exception as e:
                print("添加学生失败！", e)
                return render(request, 'dormitory/add_student.html', {"error": "添加失败！"})


def student_list(request):

    students = models.Student.objects.all()
    return render(request, 'dormitory/student_list.html', {"students": students})


def del_student(request, s_id):
    try:
        student = models.Student.objects.get(id=s_id)
        student.delete()
        return redirect(reverse('dormitory:student_list'), {"msg": "删除成功"})
    except Exception as e:
        print("删除学生信息失败！！", e)
        return redirect(reverse('dormitory:student_list'), {"msg": "删除失败！"})


def edit_student(request, s_id):
    if request.method == "GET":
        try:
            deps = models.Department.objects.all()
            student = models.Student.objects.get(id=s_id)

            return render(request, 'dormitory/edit_student.html', {"student": student, "deps": deps})
        except Exception as e:
            print("-------", e)

    else:
        # password = request.POST["password"].strip()
        name = request.POST["name"].strip()
        gender = request.POST["gender"]
        department = request.POST["department"]
        domain = request.POST["domain"]

        department = models.Department.objects.get(id=department)
        domain = models.Domain.objects.get(id=domain)

        try:
            # password = utils.pwd_by_hmac(password)
            student = models.Student.objects.get(id=s_id)
            # student.password = password
            student.name = name
            student.department = department
            student.domain = domain
            student.gender = gender
            student.save()
            return redirect(reverse('dormitory:student_list'))
            # return render(request, 'dormitory/student_list.html', {"msg": "修改成功！"})
        except Exception as e:
            print("修改学生信息失败！", e)
            # return render(request, 'dormitory/student_list.html', {"error": "修改失败！"})
            return redirect(reverse('dormitory:student_list'))


# 分配宿舍
def allot_dorm(request):
    if request.method == "GET":

        # deps = models.Department.objects.all()
        towers = models.Tower.objects.all()
        floors = models.Floor.objects.all()
        students = models.Student.objects.filter(dorm=None )
        dorms = models.Dorm.objects.all()
        # return render(request, 'dormitory/student_list.html', {"students": students, "deps": deps})

        return render(request, 'dormitory/allot_dorm.html', {"students":students, "dorms": dorms, "towers": towers, "floors":floors})
    else:
        student = request.POST["student"]
        tower = request.POST["tower"]
        floor = request.POST["floor"]
        dorm = request.POST["dorm"]

        print("1",student, tower, floor, dorm)

        student = models.Student.objects.get(id=student)
        tower = models.Tower.objects.get(id=tower)
        floor = models.Floor.objects.get(id=floor)
        dorm = models.Dorm.objects.get(id=dorm)
        print("2", student, tower, floor, dorm)
        try:
            student.tower = tower
            student.floor = floor
            student.dorm = dorm
            student.save()

            return redirect(reverse('dormitory:allot_dorm'))
        except Exception as e:
            print("分配宿舍失败！",e)


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
            request.session["deps"] = deps
            return render(request, "dormitory/add_dep.html", {"msg": "添加成功！", "deps": deps})
        except Exception as e:

            return render(request, "dormitory/add_dep.html", {"error": "该学院已存在，请重新添加！！"})


def dep_list(request):
    # 显示所有学院，并操作
    deps = models.Department.objects.all()
    # 将所有学院名称存放在session中
    request.session["deps"] = deps

    return render(request, "dormitory/dep_list.html", {"deps": deps})


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
        dep_name = request.POST["department"].strip()
        dom_name = request.POST["dom_name"].strip()


        try:

            dep = models.Department.objects.get(dep_name = dep_name)
            # print(dep.id)
            domain = models.Domain(dom_name=dom_name, department=dep)

            domain.save()

            deps = models.Department.objects.all()
            domains = models.Domain.objects.all()
            request.session["domains"] = domains
            return render(request, "dormitory/add_domain.html", {"msg": "添加成功！", "deps": deps})
        except Exception as e:
            print("-----error---", e)
            return render(request, "dormitory/add_domain.html", {"error": "该专业已存在，请重新添加！！"})


def domain_list(request):
    try:
        deps = models.Department.objects.all()
        domains = models.Domain.objects.all()
        request.session["domains"] = domains
        return render(request, 'dormitory/domain_list.html', {"domains": domains, "deps": deps})
    except Exception as e:
        print("查询全部专业出错：", e)
        return render(request, 'dormitory/domain_list.html', {"msg": "当前没有专业。"})


def del_domain(request, d_id):
    try:
        domain = models.Domain.objects.get(id=d_id)
        domain.delete()
        return redirect(reverse('dormitory:domain_list'), {"msg": "删除成功"})
    except Exception as e:
        print("删除学院失败！", e)
        return redirect(reverse('dormitory:domain_list', {"msg": "删除失败！！"}))


# 添加楼房
def add_tower(request):
    if request.method == "GET":
        try:
            towers = models.Tower.objects.all()
            return render(request, "dormitory/add_tower.html", {"towers": towers})
        except Exception as e:
            return render(request, "dormitory/add_tower.html", {"msg": "当前未添加楼房"})

    else:
        num = request.POST["num"].strip()
        sex = request.POST["sex"]

        try:
            tower = models.Tower(num=num, sex=sex)
            tower.save()
            towers = models.Tower.objects.all()
            request.session["towes"] = towers
            return render(request, "dormitory/add_tower.html", {"msg": "添加成功！", "towers": towers})
        except Exception as e:

            return render(request, "dormitory/add_tower.html", {"error": "该楼房信息已存在，请重新添加！！"})


def tower_list(request):
    try:
        towers = models.Tower.objects.all()
        request.session["towes"] = towers
        return render(request, "dormitory/tower_list.html", {"towers": towers})
    except Exception as e:
        return render(request, "dormitory/tower_list.html", {"msg": "未添加楼房信息"})


def del_tower(request, t_id):
    try:
        tower = models.Tower.objects.get(id=t_id)
        tower.delete()
        return redirect(reverse('dormitory:tower_list'), {"msg": "删除成功"})
    except Exception as e:
        print("删除楼房信息失败！", e)
        return redirect(reverse('dormitory:tower_list', {"msg": "删除失败！！"}))


# 添加楼层
def add_floor(request):
    if request.method == "GET":
        towers = models.Tower.objects.all()
        deps = models.Department.objects.all()
        domains = models.Domain.objects.all()


        return render(request, "dormitory/add_floor.html", {"towers": towers, "deps": deps, "domains": domains})
    else:
        con = request.POST["con"].strip()
        department = request.POST["department"].strip()
        domain = request.POST["domain"].strip()
        tower = request.POST["tower"].strip()
        print(con, department, domain, tower)

        try:

            dep = models.Department.objects.get(id=department)
            domain = models.Domain.objects.get(id=domain)
            tower = models.Tower.objects.get(num=tower)
            sex = tower.sex

            floor = models.Floor(con=con, sex=sex, department=dep, domain=domain, tower=tower)

            floor.save()


            # return render(request, "dormitory/add_floor.html", {"msg": "添加成功！"})
            return redirect(reverse("dormitory:add_floor"), {"msg": "添加成功！"})
        except Exception as e:
            print("-----error---", e)
            return render(request, "dormitory/add_floor.html", {"error": "该专业已存在，请重新添加！！"})


def floor_list(request):
    floors = models.Floor.objects.all()

    return render(request, 'dormitory/floor_list.html', {"floors": floors})


def del_floor(request, f_id):
    try:
        floor = models.Floor.objects.get(id=f_id)
        floor.delete()
        return redirect(reverse('dormitory:floor_list'), {"msg": "删除成功"})
    except Exception as e:
        print("删除楼层失败！")
        return redirect(reverse('dormitory:floor_list'), {"msg": "删除失败！！"})


def ajax_all_domain(request, dep):
    # 获取学院对应的字段
    print(dep)
    try:
        dep = models.Department.objects.get(id=dep)
        domains = models.Domain.objects.filter(department=dep.id)

        domains = serialize("json", domains)
        print(domains)
        # return JsonResponse({"domains": domains, "issuccess": True})
        # return JsonResponse(domains,safe=False)
        return HttpResponse(domains)
    except Exception as e:
        print("没有找到", e)
        return JsonResponse({"domains": domains, "issuccess": False})


def ajax_all_floor(request, tow_id):
    # 获取楼房对应的楼层
    print(tow_id)
    try:
        tow = models.Tower.objects.get(id=tow_id)
        floors = models.Floor.objects.filter(tower=tow.id)

        domains = serialize("json", floors)
        # print(domains)

        return HttpResponse(domains)
    except Exception as e:
        print("没有找到", e)
        return JsonResponse({"domains": floors, "issuccess": False})


# 添加宿舍
def add_dorm(request):
    if request.method == "GET":
        towers = models.Tower.objects.all()
        floor = models.Floor.objects.all()

        return render(request, 'dormitory/add_dorm.html', {"towers": towers, "floor": floor})
    else:
        suno = request.POST["suno"].strip()
        max_num = request.POST["max_num"]
        peopel = request.POST["peopel"].strip()
        floor = request.POST["floor"]
        tower = request.POST["tower"]

        tower = models.Tower.objects.get(id=tower)
        floor = models.Floor.objects.get(id=floor)
        max_num = max_num[:1]
        sex = floor.sex
        print(suno, max_num, peopel, floor, tower, sex)
        try:
            print(1)
            dorm = models.Dorm(suno=suno, max_num=max_num, people=peopel, sex=sex, floor=floor, tower=tower)
            dorm.save()
            print("添加成功")
            return redirect(reverse("dormitory:add_dorm"), {"msg": "添加成功！"})
        except Exception as e:
            print("添加宿舍信息出错:", e)
            return redirect(reverse("dormitory:add_dorm"), {"msg": "添加失败！"})


def dorm_list(request):
    try:
        dorms = models.Dorm.objects.all()
        print(dorms)
        return render(request, 'dormitory/dorm_list.html', {"dorms": dorms})
    except Exception as e:
        print("查询所有宿舍信息出错:", e)
        return render(request, 'dormitory/dorm_list.html', {"msg": "查询失败！请重试！"})


def del_dorm(request, d_id):

    try:
        dorm = models.Dorm.objects.get(id=d_id)

        dorm.delete()
        return redirect(reverse("dormitory:dorm_list"), {"msg": "删除成功！"})
    except Exception as e:
        print("删除宿舍失败！", e)
        return redirect(reverse("dormitory:dorm_list"), {"msg": "删除失败！"})


# 添加报修管理
def add_repairs(request):
    if request.method == "GET":
        return render(request, 'dormitory/add_repairs.html')

    else:
        content = request.POST["content"].strip()

        student = request.session.get("Student")

        id =student.id
        student = models.Student.objects.get(id=id)

        dorm = models.Dorm.objects.get(suno=student.dorm.suno)
        try:
            repair = models.Repairs(dorm=dorm, content=content, student=student)

            repair.save()
            return render(request, 'dormitory/add_repairs.html', {"msg":"报修成功"})
        except Exception as e:
            print("添加报修信息失败", e)
            return render(request, 'dormitory/add_repairs.html', {"error": "报修失败，请重试！"})


def my_repairs(request):
    if request.method == "GET":
        if request.session.get("Login") == "student":
            student = request.session.get("Student")
            repairs = models.Repairs.objects.filter(student=student.id)

            return render(request, "dormitory/my_repairs.html", {"repairs": repairs})
        if request.session.get("Login") == "admin":
            repairs = models.Repairs.objects.all()
            return render(request, "dormitory/my_repairs.html", {"repairs": repairs})


# 修改维修状态
def repairs_info(request, r_id):
    repair = models.Repairs.objects.get(id=r_id)
    if request.method == "GET":
        return render(request, 'dormitory/repairs_info.html', {"repair": repair})
    else:
        flag = request.POST["flag"]
        try:
            repair.flag = flag
            repair.save()
            return redirect(reverse('dormitory:my_repairs'))
        except Exception as e:
            print("修改维修状态失败！", e)
            return render(request, 'dormitory/repairs_info.html', {"repair": repair, "error":"修改状态是失败！"})




# 添加公告信息
def add_notice(request):
    if request.method == "GET":
        return render(request, 'dormitory/add_notice.html')

    else:
        title = request.POST["title"].strip()
        content = request.POST["content"].strip()

        if title == "":
            return render(request, 'dormitory/add_notice.html', {"msg_title": "标题不能为空!!!"})
        if len(title) > 150:
            return render(request, 'dormitory/add_notice.html', {"msg_title": "标题太长!!"})
        if content == "":
            return render(request, 'dormitory/add_notice.html', {"content_msg": "内容不能为空!!!"})

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
    if request.session.get("Login") == "admin":
        print(request.session.get("Login"))
        return render(request, 'dormitory/notice_list.html', {"notices": notices})
    if request.session.get("Login") == "student":
        print(request.session.get("Login"))
        return render(request, 'dormitory/student_notice.html', {"notices": notices})


def show_notice(request, n_id):
    # 显示公告内容
    # print("----1",n_id)
    try:
        notice = models.Notice.objects.get(id=n_id)
        if request.session.get("Login") == "admin":
            print("1")
            return render(request, 'dormitory/show_notice.html', {"notice": notice})
        if request.session.get("Login") == "student":
            return render(request, 'dormitory/student_notice.html', {"notice": notice})
    except Exception as e:
        print("出错了", e)
        return redirect(reverse("dormitory:notice_list"))


def ajax_notice_info(request, n_id):
    notices = models.Notice.objects.all()
    notice = models.Notice.objects.get(id=n_id)
    notice.count += 1
    notice.save()
    return render(request, 'dormitory/student_notice.html', {"notice": notice, "notices":notices})


def edit_notice(request, n_id):
    notice = models.Notice.objects.get(id=n_id)
    if request.method == "GET":

        return render(request, 'dormitory/edit_notice.html', {"notice": notice})
    else:
        title = request.POST["title"].strip()
        content = request.POST["content"].strip()

        if title == "":
            return render(request, 'dormitory/edit_notice.html', {"msg_title": "标题不能为空!!!"})
        if len(title) > 150:
            return render(request, 'dormitory/edit_notice.html', {"msg_title": "标题太长!!"})
        if content == "":
            return render(request, 'dormitory/edit_notice.html', {"content_msg": "内容不能为空!!!"})

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


def student_info(request, s_id):
    student = models.Student.objects.get(id=s_id)
    if request.method == "GET":

        return render(request, 'dormitory/student_info.html', {"student":student})
    else:
        age = request.POST["age"].strip()
        tel = request.POST["tel"].strip()

        if age == "":
            return render(request, 'dormitory/student_info.html', {"student": student,"error": "年龄不能为空！！"})

        if len(tel) == 11:
            student.age = age
            student.tel = tel
            try:
                student.save()
                return render(request, 'dormitory/student_info.html', {"student": student,"msg": "修改成功"})
            except Exception as e:
                print("修改个人信息失败", e)
                return render(request, 'dormitory/student_info.html', {"student": student, "msg": "修改失败！！"})

        else:
            return render(request, 'dormitory/student_info.html', {"student": student,"error": "手机号错误"})


# 添加意见信息
def add_suggest(request):
    if request.method == "GET":
        return render(request, 'dormitory/add_suggest.html')

    else:
        content = request.POST["content"].strip()
        anonymity = request.POST["anonymity"]
        student = request.session.get("Student")


        id = student.id
        student = models.Student.objects.get(id=id)

        dorm = models.Dorm.objects.get(suno=student.dorm.suno)
        try:
            suggest = models.Suggest(dorm=dorm, content=content, sno=student, anonymity=anonymity)

            suggest.save()
            return render(request, 'dormitory/add_suggest.html', {"msg": "提交成功"})
        except Exception as e:
            print("添加意见信息失败", e)
            return render(request, 'dormitory/add_suggest.html', {"error": "提交失败，请重试！"})


def suggest_list(request):
    """
    根据角色不同，查询的数据不同
    :param request:
    :return:
    """
    if request.session.get("Login") == "student":
        student = request.session.get("Student")
        suggests = models.Suggest.objects.filter(sno=student.id)

        return render(request, 'dormitory/suggest_list.html', {"suggests": suggests})

    if request.session.get("Login") == "admin":
        suggests = models.Suggest.objects.all()
        return render(request, 'dormitory/suggest_list.html', {"suggests": suggests})


def del_suggest(request):
    pass



# 添加水电费管理
def add_charge(request):
    pass

def del_charge(request):
    pass
