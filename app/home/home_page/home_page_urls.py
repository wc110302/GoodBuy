from django.urls import path, re_path

from app.home.home_page import home_page_api

app_name = 'home_page'
urlpatterns = [
    # 首页
    re_path(r'^home/$', home_page_api.index_page, name='home'),
    # 分类查询
    re_path(r'^list/(\d+)$', home_page_api.list_page, name='list'),

]
