# coding=utf-8

from django.conf.urls import url

from . import views

app_name = "dormitory"

urlpatterns = [

    url(r"^index/$", views.index, name="index"),
    url(r"^login/$", views.login, name="login"),
    url(r"^admin_register/$", views.admin_register, name="admin_register"),
    url(r"^add_admin/$", views.add_admin, name="add_admin"),
    url(r"^admin_list/$", views.admin_list, name="admin_list"),
    url(r"^del_admin/(?P<a_id>\d+)/$", views.del_admin, name="del_admin"),
    url(r"^reset_admin/(?P<a_id>\d+)/$", views.reset_admin, name="reset_admin"),

    url(r"^add_student/$", views.add_student, name="add_student"),
    url(r"^edit_student/(?P<s_id>\d+)/$", views.edit_student, name="edit_student"),
    url(r"^student_info/(?P<s_id>\d+)/$", views.student_info, name="student_info"),
    url(r"^student_list/$", views.student_list, name="student_list"),
    url(r"^allot_dorm/$", views.allot_dorm, name="allot_dorm"),

    url(r"^del_student/(?P<s_id>\d+)/$", views.del_student, name="del_student"),
    url(r"^add_dep/$", views.add_dep, name="add_dep"),
    url(r"^dep_list/$", views.dep_list, name="dep_list"),
    url(r"^del_dep/(?P<d_id>\d+)/$", views.del_dep, name="del_dep"),

    url(r"^add_domain/$", views.add_domain, name="add_domain"),
    url(r"^domain_list/$", views.domain_list, name="domain_list"),
    url(r"^del_domain/(?P<d_id>\d+)/$", views.del_domain, name="del_domain"),

    url(r"^add_tower/$", views.add_tower, name="add_tower"),
    url(r"^tower_list/$", views.tower_list, name="tower_list"),
    url(r"^del_tower/(?P<t_id>\d+)/$", views.del_tower, name="del_tower"),

    url(r"^add_floor/$", views.add_floor, name="add_floor"),
    url(r"^floor_list/$", views.floor_list, name="floor_list"),
    url(r"^del_floor/(?P<f_id>\d+)/$", views.del_floor, name="del_floor"),

    url(r"^add_dorm/$", views.add_dorm, name="add_dorm"),
    url(r"^dorm_list/$", views.dorm_list, name="dorm_list"),
    url(r"^del_dorm/(?P<d_id>\d+)/$", views.del_dorm, name="del_dorm"),
    url(r"^add_repairs/$", views.add_repairs, name="add_repairs"),
    url(r"^add_charge/$", views.add_charge, name="add_charge"),
    url(r"^del_charge/$", views.del_charge, name="del_charge"),

    url(r"^add_notice/$", views.add_notice, name="add_notice"),
    url(r"^notice_list/$", views.notice_list, name="notice_list"),
    url(r"^show_notice/(?P<n_id>\d+)/$", views.show_notice, name="show_notice"),
    url(r"^edit_notice/(?P<n_id>\d+)/$", views.edit_notice, name="edit_notice"),
    url(r"^del_notice/(?P<n_id>\d+)/$", views.del_notice, name="del_notice"),

    url(r"^add_suggest/$", views.add_suggest, name="add_suggest"),
    url(r"^suggest_list/$", views.suggest_list, name="suggest_list"),
    url(r"^del_suggest/$", views.del_suggest, name="del_suggest"),

    # 验证码
    url(r"^code/$", views.code, name="code"),
    url(r"logout/$", views.logout, name="logout"),

    # 添加楼层走的ajax
    url(r"^ajax_all_domain/(?P<dep>\d+)/$", views.ajax_all_domain, name="ajax_all_domain"),
    # 添加宿舍走的ajax
    url(r"^ajax_all_floor/(?P<tow_id>\d+)/$", views.ajax_all_floor, name="ajax_all_floor"),

    url(r"^ajax_notice_info/(?P<n_id>\d+)/$", views.ajax_notice_info, name="ajax_notice_info"),
    # 报修
    url(r"^my_repairs/$", views.my_repairs, name="my_repairs"),
    url(r"^repairs_info/(?P<r_id>\d+)/$", views.repairs_info, name="repairs_info"),



]