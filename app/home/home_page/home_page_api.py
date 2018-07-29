"""
前台首页
AUTH:
DATE:
"""
import random

from django.shortcuts import render
from django.http.response import HttpResponse

# 首页
from django.views.decorators.cache import cache_page

from app.models import Classification, Subclassification, Goods, Hot


@cache_page(60*10)
def index_page(request):
    if request.method == 'GET':
        # 大类分类
        classification = Classification.objects.all()
        # 小类分类
        subclassification = Subclassification.objects.all()
        # 商品
        mylist = [random.randint(34,26124) for _ in range(30)]
        goods = Goods.objects.filter(id__in=mylist)
        # 热门搜索
        hots = Hot.objects.all()

        data = {
            'classification': classification,
            'subclassification': subclassification,
            'goods': goods
        }
        return render(request, 'home/index.html', data)


# 分类查询
def list_page(request, cid):
    if request.method == 'GET':
        # 小类分类
        subclassification = Subclassification.objects.get(id=cid)
        # 大类分类
        classification = Classification.objects.filter(id=subclassification.classification_id)
        # 商品筛选
        goods = Goods.objects.filter(subclassification_id=cid)

        data = {
            'classification': classification,
            'subclassification': subclassification,
            'goods': goods
        }
        return render(request, 'home/list.html', data)
