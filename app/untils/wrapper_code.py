"""
装饰器类,访问页面,登录验证,接口访问登录验证
AUTH: Jason
DATE: 2018年7月5日 09:49:38
"""

from functools import wraps
from django.http.response import HttpResponseRedirect


def is_login(fn):
    """
    访问页面时的登录的验证
    未登录会跳转到登录页面
    :param fn:  需要判断的方法
    :return: 返回具体页面
    """

    @wraps(fn)
    def wrapper(request, *args, **kwargs):
        try:
            user = request.session['admin_user_name']
            print(user)
        except KeyError as e:
            return HttpResponseRedirect('/admin_page/login/', {'msg':'请先登录'})
        else:
            return fn(request, *args, **kwargs)

    return wrapper