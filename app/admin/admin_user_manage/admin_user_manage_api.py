"""
管理员账户管理页面
AUTH:
DATE:
"""

from django.shortcuts import render
from django.http.response import JsonResponse, HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from app.models import AdminUser

# def admin_user_manage(request):
#     return render(request, 'Hello world')
from app.untils.wrapper_code import is_login


@is_login
def user_list(request):
    # 管理员列表
    super_name = AdminUser.objects.all()
    is_root = ''
    if request.session['admin_user_name'] == 'root':
        is_root = 'yes'
    data = {
        'super_name': super_name,
        'is_root': is_root
    }
    return render(request, 'admin/userList.html', data)

@is_login
def look_user(request):
    # 查看管理员账号密码
    data = request.POST
    myName = data.get('myName')

    if myName:

        look = AdminUser.objects.filter(username=myName).first()
        password = look.password

        data = {
            'code': 200,
            'username': myName,
            'password': password
        }
        return JsonResponse(data)

    data = {
        'code': 200,
        'password': '没东西给你,滚!'
    }

    return JsonResponse(data)

@is_login
def delete_user(request):
    # 删除该管理员账号
    myName = request.POST.get('myName')
    look = AdminUser.objects.filter(username=myName).first()
    look.delete()
    data = {
        'code': 200,
        'msg': '删除成功!'
    }
    return JsonResponse(data)



@is_login
def user_add_page(request):
    # 添加管理员页面
    is_root = ''
    msg = ''
    if request.session['admin_user_name'] == 'root':  # 判断是否为root超级管理员 id = 1
        is_root = 'OK'
        msg = '欢迎超级管理员!'
    return render(request, 'admin/userAddPage.html', {'msg': msg, 'is_root': is_root})


@is_login
def user_add(request):
    # 添加管理员按钮
    is_root = ''
    if request.method == 'GET':
        return HttpResponseRedirect('/admin_user_manage/userAddPage/')

    if request.method == 'POST':
        if request.session['admin_user_name'] == 'root':
            is_root = 'OK'
            username = request.POST.get('username')
            password = request.POST.get('password')
            if not all([username, password]):
                msg = '用户名或密码不能为空'
                return render(request, 'admin/userAddPage.html', {'msg': msg, 'is_root': is_root})
            # 判断用户名是否存在
            admin_list = AdminUser.objects.all()
            for admin in admin_list:
                if username == admin.username:
                    return render(request, 'admin/userAddPage.html', {'msg': '用户已存在', 'is_root': is_root})
            # 判断密码长度
            if len(password) < 6:
                return render(request, 'admin/userAddPage.html', {'msg': '密码长度过短(建议6位及以上)', 'is_root': is_root})
            # 密文存储
            password = make_password(password)
            AdminUser.objects.create(username=username,
                                     password=password,
                                     )
            return render(request, 'admin/userAddPage.html', {'msg': '添加成功', 'is_root': is_root})
        else:
            is_root = ''
            return render(request, 'admin/userAddPage.html', {'msg': '你是哪根葱?', 'is_root': is_root})


@is_login
def edit_user_psd(request):
    if request.method == 'GET':
        return HttpResponseRedirect('/admin_user_manage/userList/')
    if request.method == 'POST':
        username = request.POST.get('myName')
        password = request.POST.get('psd')
        this_user = AdminUser.objects.get(username=username)
        this_user.password = make_password(password)
        this_user.save()
        data = {
            'code': 200,
            'msg': '修改成功'
        }

        return JsonResponse(data)

