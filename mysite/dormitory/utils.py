# coding=utf-8

import hashlib
import hmac
import random
import string
import re
import time
from datetime import datetime

from django.shortcuts import render
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont, ImageFilter


# 登录验证
def require_login(fn):
    """
    用来判断用户是否登录的装饰器
    :param fn: 视图函数
    :return: 如果已经登录，则进入视图函数，否则返回登录页面
    """
    def inner(request, *args, **kwargs):
        # 判断session是否存在登录用户
        login_user = request.session.get("loginUser", None)
        if login_user is not None:
            return fn(request, *args, **kwargs)

        else:
            # 将页面返回到登录页面
            return render(request, 'blog/login.html', {"msg": "请登录！"})

    return inner


# 密码加密
def pwd_by_hashlib(password):

    """
    使用hashlib模块完成对用户密码加密操作, 做摘要一般用这个
    :param password: 用户面
    :return: 返回加密后的密文
    """
    md5 = hashlib.md5(password.encode("utf-8"))
    md5.update(settings.SALT.encode("utf-8"))
    return md5.hexdigest()


# 密码加密
def pwd_by_hmac(password):

    """
    使用hmac模块完成对用户密码的加密，密码加密用这个更安全
    :param password: 用户密码
    :return: 返回加密后的密文
    """
    password = hmac.new(settings.SALT.encode("utf-8"), password.encode("utf-8"), "MD5").hexdigest()
    # password = hmac.new("@du#abc$qwe&".encode("utf-8"), password.encode("utf-8"), "MD5").hexdigest()

    return password


# 以下是验证码功能
def get_random_char(count=4):
    # 生成随机字符串
    # string模块 一下为小写字母、大写字母和数字
    ran = string.ascii_lowercase + string.ascii_uppercase + string.digits
    char = ''
    for i in range(count):
        char += random.choice(ran)
    return char


def get_random_color():
    # 返回一个随机的RGB颜色
    # return random.randint(200, 255), random.randint(200, 255), random.randint(200, 255)
    return random.randint(50, 155), random.randint(50, 155), random.randint(50, 155)


def creat_code():
    # 创建图片， 模式，大小，背景颜色
    img = Image.new("RGB", (120, 30), (255, 255, 255))
    # 创建画布
    draw = ImageDraw.Draw(img)
    # 设置字体
    font = ImageFont.truetype("arial.ttf", 25)

    code = get_random_char()
    # 将生成的字符画在画布上
    for t in range(4):
        draw.text((30*t+5, 0), code[t], get_random_color(), font)

    # 生成干扰点
    for i in range(random.randint(500, 650)):
        # 位置，颜色
        draw.point((random.randint(0, 120), random.randint(0, 30)), fill=get_random_color())
    # 使用模糊滤镜使图片模糊
    # img = img.filter(ImageFilter.BLUR)
    # 可以保存，这里不使用
    # img.save(''.join(code)+'.jpg', 'jpeg')
    return img, code


# 生成文章摘要
def abstract(content):
    print(content)

    # a = re.findall(r"<([a-zA-Z]*)>(.*?)</\1>", content)  # 简单匹配 不带标签属性
    # a =re.findall(r">(.*?)<",content)
    pre = re.compile('>(.*?)<')
    #
    str = ''.join(pre.findall(content))
    print(str)
    print(str[:50])
    str = str[:50]
    return str



