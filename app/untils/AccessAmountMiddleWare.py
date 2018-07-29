import re
import time

import redis
from django.utils.deprecation import MiddlewareMixin

from GoodBuy.settings import SESSION_REDIS


class AccessAmountMiddleware(MiddlewareMixin):
    """
    访问量中间件
    """
    conn = redis.StrictRedis(host=SESSION_REDIS['host'], port=SESSION_REDIS['port'], password=SESSION_REDIS['password'], decode_responses=True)

    # 增加访问量并保存redis
    def SaveToRedis(self, name):
        mydict = eval(self.conn.hget('access', time.strftime("%Y-%m-%d")))
        mydict[name] = mydict[name] + 1
        self.conn.hset('access', time.strftime("%Y-%m-%d"), mydict)

    # 访问量中间件
    def process_request(self, request):
        if not self.conn.hexists('access', time.strftime("%Y-%m-%d")):
            data = {'首页': 0, '搜索页面': 0, '商品页面': 0, '个人中心页面': 0, '登录页面': 0, '注册页面': 0}
            self.conn.hset('access', time.strftime("%Y-%m-%d"), data)
        if request.path == '/index/':
            self.SaveToRedis('首页')
        if re.search('/search/', request.path):
            self.SaveToRedis('搜索页面')
        if re.search('/goods/', request.path):
            self.SaveToRedis('商品页面')
        if request.path == '/user/user_home/':
            self.SaveToRedis('个人中心页面')
        if request.path == '/user/user_login/':
            self.SaveToRedis('登录页面')
        if request.path == '/user/user_register/':
            self.SaveToRedis('注册页面')
