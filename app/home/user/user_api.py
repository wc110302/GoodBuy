"""
用户
AUTH:
DATE:
"""
import re
import time
from datetime import datetime, timedelta

import qiniu
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.http import require_GET,require_POST
from qiniu import etag

from GoodBuy.settings import ACCESS_KEY, BASE_DIR, BUCKET_NAME, AVATAR_DIR, QINIU_SECRET_KEY
from app.models import UserTicket, User, Focus, Comments
from app.untils.functions import get_ticket, get_user


def user_register(request):
    if request.method == 'GET':
        return render(request, 'home/user/register.html')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        code = request.POST.get('checkcode')

        if not all([username, password, password2, code]):
            msg = '参数不能为空'
            return render(request, 'home/user/register.html', {'msg': msg})

        if password != password2:
            msg = '两次密码不一致'
            return render(request, 'home/user/register.html', {'msg': msg})

        if code != request.session['v_code']:
            msg = '验证码错误'
            return render(request, 'home/user/register.html', {'msg': msg})

        if User.objects.filter(username=username).first():
            msg = '用户名已被注册'
            return render(request, 'home/user/register.html', {'msg': msg})

        hash_password = make_password(password)
        User.objects.create(username=username,
                            password=hash_password,
                            icon='http://pbu0s2z3p.bkt.clouddn.com/static/icon/hello.jpg'
                            )
        return HttpResponseRedirect('/user/user_login/')


def user_login(request):
    if request.method == 'GET':
        return render(request, 'home/user/login.html')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        code = request.POST.get('checkcode')
        # 验证用户是否存在
        if code != request.session['v_code']:
            msg = '验证码不正确'
            return render(request, 'home/user/login.html', {'msg': msg})

        user = User.objects.filter(username=username).first()
        if user:
            # 验证密码是否正确

            if check_password(password, user.password):
                # 1. 保存ticket在客户端
                ticket = get_ticket()
                response = HttpResponseRedirect('/user/user_home/')
                out_time = datetime.now() + timedelta(days=1)
                response.set_cookie('ticket', ticket, expires=out_time)
                # 2. 保存ticket到服务端的user_ticket表中
                UserTicket.objects.create(user=user,
                                          out_time=out_time,
                                          ticket=ticket)
                request.session['username'] = user.username

                return response
            else:
                msg = '用户名或密码错误'
                return render(request, 'home/user/login.html', {'msg': msg})
        else:
            msg = '用户名或密码错误'
            return render(request, 'home/user/login.html', {'msg': msg})


def user_logout(request):
    if request.method == 'GET':
        # 注销，删除当前登录的用户的cookies中的ticket信息
        response = HttpResponseRedirect('/user/user_login/')
        response.delete_cookie('ticket')

        return response


def user_home(request):
    user = get_user(request)

    if request.method == 'GET':
        data = {'user': user}

        return render(request, 'home/user/user_home.html', data)
    if request.method == 'POST':
        username = request.POST.get('username')
        icon = request.FILES['icon']
        email = request.POST.get('email')
        sex = request.POST.get('sex')
        tel = request.POST.get('tel')

        if username and username != user.username:
            if User.objects.filter(username=username).first():
                msg = '用户名已存在'
                return render(request, 'home/user/user_home.html', {'msg': msg})
            user.username = username

        if email and email != user.email:
            if User.objects.filter(email=email).first():
                msg = '该邮箱已注册'
                return render(request, 'home/user/user_home.html', {'msg': msg})
            if not re.match("^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$", str(email)):
                msg = '请输入有效邮箱号'
                return render(request, 'home/user/user_home.html', {'msg': msg})
            user.email = email

        if icon:
            with open(BASE_DIR + AVATAR_DIR, 'wb') as pic:
                for c in icon.chunks():
                    pic.write(c)
            # 构建鉴权对象
            q = qiniu.Auth(ACCESS_KEY, QINIU_SECRET_KEY)
            # 上传到七牛后保存的文件名
            key = 'static/icon/' + user.username + '/'+str(time.time())+'.jpg'
            # 生成上传 Token，可以指定过期时间等
            token = q.upload_token(BUCKET_NAME, key)
            localfile = BASE_DIR + '/static/images/icon.jpg'
            qiniu.put_file(token, key, localfile)
            user.icon = 'http://pbu0s2z3p.bkt.clouddn.com/' + key

        if tel and tel != user.tel:
            if User.objects.filter(tel=tel).first():
                msg = '该手机已注册'
                return render(request, 'home/user/user_home.html', {'msg': msg})
            if not re.match("^(13[0-9]|14[579]|15[0-3,5-9]|16[6]|17[0135678]|18[0-9]|19[89])\d{8}$", str(tel)):
                msg = '请输入有效手机号'
                return render(request, 'home/user/user_home.html', {'msg': msg})
            user.tel = tel

        if sex and sex != user.sex:
            user.sex = 1 if sex == '男' else 0
        user.save()
        return HttpResponseRedirect('/user/user_home/')


def user_collection(request):
    user = get_user(request)
    focus = Focus.objects.filter(user=user)
    goods = []
    for f in focus:
        goods.append(f.goods)
    data = {'goods': goods}
    return render(request, 'home/user/collection.html', data)


def user_comment(request):
    user = get_user(request)
    comments = Comments.objects.filter(user=user)
    data = {'comments': comments}
    return render(request, 'home/user/comment.html', data)


def user_icon(request):
    if request.method == 'GET':
        return render(request, 'home/user/icon.html')
    if request.method == 'POST':
        file = request.FILES['avatar']
        with open(BASE_DIR+'/static/images/icon.jpg', 'wb') as pic:
            for c in file.chunks():
                pic.write(c)
        user = get_user(request)
        # 要上传的空间
        bucket_name = 'goodbuy'
        # 构建鉴权对象
        q = qiniu.Auth(ACCESS_KEY, QINIU_SECRET_KEY)
        # 上传到七牛后保存的文件名
        key = 'static/icon/'+user.username+'3.jpg'
        # 生成上传 Token，可以指定过期时间等
        token = q.upload_token(bucket_name, key)
        localfile = BASE_DIR+'/static/images/icon.jpg'
        ret, info = qiniu.put_file(token, key=key, file_path=localfile)
        print(info, ret)
        assert ret['key'] == key
        assert ret['hash'] == etag(localfile)
        user.icon = 'http://pbu0s2z3p.bkt.clouddn.com/'+key
        user.save()
        return JsonResponse({'key':key,'token':token})