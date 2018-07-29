from datetime import datetime

from django.db.models import Q
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin

from app.models import UserTicket


class UserMiddle(MiddlewareMixin):
    
    @staticmethod
    def process_request(request):

        # 需要登录验证的URL
        need_login = ['/user/user_home/', '/user/icon/', '/user_logout/', '/user_collection/', '/user_comment/']
        if request.path in need_login:
            # 先获取cookies中的ticket参数
            ticket = request.COOKIES.get('ticket')
            # 如果没有ticket，则直接跳转到登录
            if not ticket:
                return HttpResponseRedirect('/user/user_login/')

            user_ticket = UserTicket.objects.filter(ticket=ticket).first()
            if user_ticket:
                # 获取到有认证的相关信息
                # 1. 验证当前认证信息是否过期，如果没过期，request.user赋值
                # 2. 如果过期了，跳转到登录，并删除认证信息
                if datetime.utcnow() > user_ticket.out_time.replace(tzinfo=None):
                    # 过期
                    UserTicket.objects.filter(user=user_ticket.user).delete()
                    return HttpResponseRedirect('/user/user_login/')
                else:
                    # 没有过期，赋值request.user，并且删除多余的认证信息
                    request.user = user_ticket.user
                    # 删除多余的认证信息，
                    # 从UserTicket中查询当前user，并且ticket不等于cookie中的ticket
                    UserTicket.objects.filter(Q(user=user_ticket.user) &
                                              ~Q(ticket=ticket)).delete()
                    return None
            else:
                return HttpResponseRedirect('/user/user_login/')
        else:
            return None
