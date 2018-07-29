from django.urls import path
from django.conf.urls import url


from app.home.goods import goods_api

urlpatterns = [
    url('^detail/(?P<pk>[0-9]+)/$', goods_api.goods),
    path('/goods/', goods_api.goods_list),
    url(r'^items/(?P<pk>[0-9]+)/$', goods_api.goods_detail),
    url(r'^focus/', goods_api.focus),
    url(r'^is_focus/(?P<pk>[0-9]+)/$', goods_api.is_focus),
    url(r'^history/(?P<pk>[0-9]+)/$', goods_api.history_data),
    url(r'^comments/(?P<pk>[0-9]+)/$', goods_api.comments),
]
