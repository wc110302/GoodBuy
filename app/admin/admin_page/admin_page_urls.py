from django.urls import path

from app.admin.admin_page import admin_page_api

urlpatterns = [
    # 后台登录
    path('login/', admin_page_api.login),
    # 后台首页
    path('index/', admin_page_api.admin_page),
    # 退出
    path('logout/', admin_page_api.logout),
    # 后台首页内容区域
    path('main/', admin_page_api.admin_main),
    # 后台头部
    path('top/', admin_page_api.admin_top),
    # 后台菜单
    path('menu/', admin_page_api.admin_menu),
    # 访问量
    path('main_access/', admin_page_api.admin_main_access),
    path('main_access2/', admin_page_api.admin_main_access2),
    # 热门对比
    path('main_hotword/', admin_page_api.admin_main_hotword),
    # 商品收藏统计
    path('main_focus/', admin_page_api.admin_focus_goods),
]