"""
搜索页面
AUTH:
DATE:
"""
import re


from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET

from app.models import Goods, Hot


def index(request):
    if request.method == 'GET':
        return render(request, '../templates/home/index.html')

@require_GET
def search_goods(request):

    key = request.GET.get('key', None)
    brand = request.GET.get('brand', None)
    sort = request.GET.get('sort', 0)
    page = int(request.GET.get('page', 1))

    if not key or key=='None':
        goods = Goods.objects.all()
        brands = None
    else:
        # 过滤
        # key = re.sub('[^\u4e00-\u9fa5_a-zA-Z0-9]', '', key)

        if Hot.objects.filter(word=key).first():
            hot = Hot.objects.filter(word=key).first()
            hot.count += 1
            hot.save()
        else:
            Hot.objects.create(word=key, count=1)

        goods = Goods.objects.filter(name__icontains=key)
        brands = goods.filter(brand__isnull=False).values('brand__name').annotate(Count('brand'))

    # 筛选
    if brand!='None' and brand:
        goods = goods.filter(brand__name=brand)

    page_num = (len(goods)//20)+1

    if page < 0 or page > page_num:
        page_list=[]
    if page_num <= 7:
        page_list = list(range(1,page_num+1))
    elif page <= 5:
        page_list = list(range(1,8))
        page_list.append(None)
    elif page_num - page > 3:
        page_list = [1, 2, None] + list(range(page-2, page+3))
        page_list.append(None)
    else:
        page_list = [1, 2, None] + list(range(page_num-4, page_num+1))



    if sort == '0':
        # 默认排序
        goods = goods.order_by('sales_number')
    elif sort == '1':
        # 价格升序
        goods = goods.order_by('c_price')
    elif sort == '2':
        # 价格降序
        goods = goods.order_by('-c_price')
    elif sort == '3':
        # 全网评论数排序
        goods = goods.order_by('-comments_amount')
    goods = goods[(page-1)*20:page*20]

    data = {
        'goods': goods,
        'brands': brands,
        'brand': brand,
        'sort': sort,
        'key': key,
        'page_list': page_list,
        'page': page,
        'page_num':page_num
    }
    return render(request, 'home/list.html', data)

    # if request.method == 'GET':
    #     key = request.GET.get('key')
    #     source = request.GET.get('source')
    #     sort = request.GET.get('sort', 0)
    #     page_id = request.GET.get('page_id', 1)
    #     if key:
    #         # 过滤关键字的特殊符号
    #         filter_key = re.sub('[^\u4e00-\u9fa5_a-zA-Z0-9]', '', key)
    #         # 使用jieba分词将关键字进行分词
    #         # all_key = jieba.cut_for_search(filter_key)
    #
    #         subclass = Subclassification.objects.filter(name=filter_key).first()
    #         sub_brands = subclass.subclassificationbrand_set.all() if subclass else None
    #         sub_classes = None
    #         if subclass:
    #             goods = subclass.goods_set.all()
    #         else:
    #             firclass = Classification.objects.filter(name__icontains=filter_key).first()
    #             class_list = firclass.subclassification_set.all() if firclass else None
    #             if class_list:
    #                 # 能搜索到一级分类
    #                 firclass_list = []
    #                 for cla in class_list:
    #                     firclass_list.append(cla.id)
    #                 goods = Goods.objects.filter(subclassification_id__in=firclass_list)
    #                 # 一级分类下的二级分类
    #                 sub_classes = Subclassification.objects.filter(id__in=class_list)
    #             else:
    #                 goods = Goods.objects.filter(name__icontains=filter_key)
    #         if sort == '0':
    #             # 默认排序
    #             goods = goods.order_by('id')
    #         elif sort == '1':
    #             # 价格升序
    #             goods = goods.order_by('c_price')
    #         elif sort == '2':
    #             # 价格降序
    #             goods = goods.order_by('-c_price')
    #         elif sort == '3':
    #             # 全网评论数排序
    #             goods = goods.order_by('-comments_amount')
    #         # 把商品进行分页处理, 每页2条数据
    #         page_count = 2
    #         paginator = Paginator(goods, page_count)
    #         page = paginator.page(int(page_id))
    #         return render(request, 'home/list.html', {'goods': page,
    #                                                                'key': filter_key,
    #                                                                'sort': sort,
    #                                                                'page_id': page_id,
    #                                                                'sub_brands': sub_brands,
    #                                                                'sub_classes': sub_classes,
    #                                                                'page_count': page_count})
    #     return render(request, 'home/list.html',{'goods':Goods.objects.all()})
    #

# 分类搜索
@require_GET
def classification_search(request):
    subcalss = request.GET.get('subcalss')
