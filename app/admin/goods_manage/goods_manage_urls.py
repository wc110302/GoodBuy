from django.urls import path

from app.admin.goods_manage import goods_manage_api

urlpatterns = [
    path('goodsList/',goods_manage_api.goods_list),
    path(r'goodsList/?page=(\d+)/', goods_manage_api.goods_list),
    path('goodsAdd/', goods_manage_api.goods_add),
    path('goodsSearch/', goods_manage_api.goods_search),
    path('goodsRemove/', goods_manage_api.goods_remove),
    path('categoryList/', goods_manage_api.category_list),
    path(r'categoryList/?page=(\d+)/', goods_manage_api.category_list),
    path('categoryAdd/', goods_manage_api.category_add),
    path('categoryChange/', goods_manage_api.category_change),
    path('categoryRemove/', goods_manage_api.category_remove),
    path('brandList/', goods_manage_api.brand_list),
    path(r'brandList/?page=(\d+)/', goods_manage_api.brand_list),
    path('brandAdd/', goods_manage_api.brand_add),
    path('brandChange/', goods_manage_api.brand_change),
    path('brandRemove/', goods_manage_api.brand_remove),
    path('brandSearch/', goods_manage_api.brand_search),

]