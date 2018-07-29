"""
后台页面
AUTH: jason
DATE: 2018.07.07
"""
import time

from django.contrib.auth.hashers import check_password
from django.core import serializers
from django.db.models import Count
from django.shortcuts import render
from django.http.response import JsonResponse, HttpResponseRedirect
import redis
from django.views.decorators.http import require_GET, require_http_methods

from GoodBuy.settings import SESSION_REDIS
from app.models import AdminUser, Hot, Focus
from app.untils.wrapper_code import is_login

# 后台登录
@require_http_methods(['GET','POST'])
def login(request):
    if request.method == 'GET':
        return render(request, 'admin/login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        v_code = request.POST.get('verify_code_text')
        data = {}
        if not all([username, password, v_code]):
            data['code'] = 1001
            data['msg'] = '参数错误'
            return render(request, 'admin/login.html', data)
        if v_code.lower() != request.session['v_code']:
            data['code'] = 1002
            data['msg'] = '验证码错误'
            return render(request, 'admin/login.html', data)
        try:
            user = AdminUser.objects.filter(username=username).first()
            if not user:
                data['code'] = 1003
                data['msg'] = '账号或密码错误'
                return render(request, 'admin/login.html', data)
            if  not check_password(password, user.password):
                data['code'] = 1004
                data['msg'] = '账号或密码错误'
                return render(request, 'admin/login.html', data)
            request.session['admin_user_name'] = user.username
            data['code'] = 200
            data['user_id'] = user.id
            return HttpResponseRedirect('/admin_page/index/')
        except Exception:
            data['code'] = 1005
            data['msg'] = '未知错误'
            return render(request,'admin/login.html',data)

# 后台首页
@is_login
@require_GET
def admin_page(request):
    return render(request, 'admin/index.html')

# 后台头部
@is_login
@require_GET
def admin_top(request):
    return render(request, 'admin/top.html',
                  {'admin_user_name':request.session['admin_user_name']})

# 后台左边菜单
@is_login
@require_GET
def admin_menu(request):
    return render(request, 'admin/menu.html')

# 后台右边内容
@is_login
@require_GET
def admin_main(request):
    return render(request, 'admin/main.html')

# 各页面访问量统计
@is_login
@require_GET
def admin_main_access(request):
    data = {}
    try:
        conn = redis.StrictRedis(host=SESSION_REDIS['host'], port=SESSION_REDIS['port'], password=SESSION_REDIS['password'],decode_responses=True)
        access = conn.hgetall('access')
        access_amount = [0] * 6
        for val in access.values():
            for i,num in enumerate(eval(val).values()):
                access_amount[i] += num
        data['access_amount'] = access_amount
        data['access_name'] = ['首页', '搜索页面', '商品页面', '个人中心页面', '登录页面', '注册页面']
        data['code'] = 200
        return JsonResponse(data)
    except Exception:
        data['code'] = 1101
        data['msg'] = '数据获取失败，请重新加载'
        return JsonResponse(data)

# 各时间段访问量统计
@require_GET
def admin_main_access2(request):
    data = {}
    try:
        conn = redis.StrictRedis(host=SESSION_REDIS['host'], port=SESSION_REDIS['port'], password=SESSION_REDIS['password'], decode_responses=True)
        choice_time = request.GET.get('choice_time')
        choice_date = request.GET.get('choice_date', '1')
        today = time.strftime("%Y-%m-%d")
        data['code'] = 200
        data['today'] = today
        access = conn.hgetall('access')
        if choice_time:
            access_time_dict = eval(access[choice_time])
            data['access_amount'] = list(access_time_dict.values())
            data['access_name'] = list(access_time_dict.keys())
            return JsonResponse(data)

        if choice_date == '1':
            access = dict(sorted(list(access.items()))[-7:])
        if choice_date == '2':
            access = dict(sorted(list(access.items()))[-30:])
        if choice_date == '3':
            access = dict(sorted(list(access.items()))[-90:])
        data['access_name'] = list(access.keys())
        access_amount = []
        for val in access.values():
            count = 0
            for num in eval(val).values():
                count += num
            access_amount.append(count)
        data['access_amount'] = access_amount
        return JsonResponse(data)
    except Exception:
        data['code'] = 1501
        data['msg'] = '数据获取失败，请重新加载'
        return JsonResponse(data)


# 热门对比词汇统计
@is_login
@require_GET
def admin_main_hotword(request):
    data = {}
    try :
        hotwords = Hot.objects.filter().order_by('-count')[:6]
        hotwords_list = [{'value': i.count, 'name': i.word} for i in hotwords]
        data['code'] = 200
        data['hotwords'] = hotwords_list
        return JsonResponse(data)
    except Exception:
        data['code'] = 1301
        data['msg'] = '服务器不堪重负了'

    return JsonResponse(data)

# 收藏商品统计
@is_login
@require_GET
def admin_focus_goods(request):
    data = {}
    try:
        focus = Focus.objects.filter()
        all_focus_goods = focus.annotate(sum=Count('goods_id')).values('goods_id','sum','goods__name')
        focus_goods = list(all_focus_goods.order_by('-sum')[:6])
        data['code'] = 200
        data['focus'] = focus_goods
        return JsonResponse(data)
    except Exception:
        data['code'] = 1401
        data['msg'] = '服务器加载失败'

# 退出登录
@require_GET
def logout(request):
    del request.session['admin_user_name']
    return HttpResponseRedirect('/admin_page/index/')

