"""
后台商品管理页面
AUTH:
DATE:
"""
from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse, HttpResponseRedirect
from app.models import Goods, Brand, Classification, SubclassificationBrand
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# 分页里每页展示的数据数量
PAGE_DATA_NUMBER = 20

def goods_list(request):
    # 商品列表
    goods_list = Goods.objects.all()
    brandlist = Brand.objects.all()
    classification = Classification.objects.all()

    # 生成paginator对象,定义每页显示1条记录
    paginator = Paginator(goods_list, PAGE_DATA_NUMBER)
    # 从前端获取当前的页码数,默认为1
    page = request.GET.get('page', 1)

    # 把当前的页码数转换成整数类型
    page = int(page)
    try:
        goods_lists = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        goods_lists = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        goods_lists = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

    # data_num 当前页数据数目
    data_num = len(paginator.page(page).object_list)

    # page为当前页
    data = {
        'goods_lists': goods_lists,
        'page': page,
        'p': paginator,
        'data_num': data_num,
        'brandlist': brandlist,
        'classification': classification

    }
    return render(request, 'admin/goodsList.html', data)


def goods_add(request):
    # 添加商品
    msg = ''
    if request.method == 'POST':
        name = request.POST.get('name')
        c_price = request.POST.get('c_price')
        image = request.POST.get('image')
        description = request.POST.get('description')
        comments_amount = request.POST.get('comments_amount')
        sales_number = request.POST.get('goods_number')
        source = request.POST.get('source')
        subclassification_id = request.POST.get('cat_id')
        brand_id = request.POST.get('brand_id')

        Goods.objects.create(
            name=name,
            c_price=c_price,
            image=image,
            description=description,
            comments_amount=comments_amount,
            sales_number=sales_number,
            source=source,
            subclassification_id=subclassification_id,
            brand_id=brand_id
        )

        msg = '添加成功!'

    brand_lists = Brand.objects.all()
    classification_list = Classification.objects.all()

    data = {
        'brand_list': brand_lists,
        'classification_list': classification_list,
        'msg': msg
    }

    return render(request, 'admin/goodsAdd.html', data)


def goods_remove(request):
    # 删除商品
    if request.method == 'GET':
        return HttpResponseRedirect('/goods_manage/goodsList/')
    if request.method == 'POST':
        name = request.POST.get('myName')
        goods = Goods.objects.filter(name=name).first()
        goods.delete()
        data = {
            'code': 200,
            'msg': '删除成功'
        }

        return JsonResponse(data)



def goods_search(request):
    # 商品组合查询
    if request.method == 'GET':
        return HttpResponseRedirect('/goods_manage/goodsList/')
    if request.method == 'POST':
        cat_id = request.POST.get('cat_id')
        brand_id = request.POST.get('brand_id')
        keyword = request.POST.get('keyword')
        # 注意 cat_id 与 brand_id 传入进来的时候是str eg: '0' '1' '2'
        if any([int(cat_id), int(brand_id), keyword]):
            # 判断条件 keyword -- 名字,描述 cat_id 分类 brand_id 品牌
            if not keyword and not int(cat_id):
                goodslist = Goods.objects.filter(brand_id=brand_id)
            if not keyword and not int(brand_id):
                goodslist = Goods.objects.filter(subclassification_id=cat_id)
            if not int(brand_id) and not int(cat_id):
                goodslist = Goods.objects.filter(Q(name__contains=keyword)|Q(description__contains=keyword))
            if int(brand_id) and int(cat_id):
                goodslist = Goods.objects.filter(Q(subclassification_id=cat_id)&Q(brand_id=brand_id))
            if int(brand_id) and keyword:
                goodslist = Goods.objects.filter((Q(name__contains=keyword)|Q(description__contains=keyword))&Q(brand_id=brand_id))
            if int(cat_id) and keyword:
                goodslist = Goods.objects.filter((Q(name__contains=keyword)|Q(description__contains=keyword))&Q(brand_id=brand_id))
            if int(cat_id) and int(brand_id) and keyword:
                goodslist = Goods.objects.filter(Q(subclassification_id=cat_id), (Q(name__contains=keyword)|Q(description__contains=keyword))&Q(brand_id=brand_id))
            brandlist = Brand.objects.all()
            classification = Classification.objects.all()
            # 生成paginator对象,定义每页显示1条记录
            paginator = Paginator(goodslist, PAGE_DATA_NUMBER)
            # 从前端获取当前的页码数,默认为1
            page = request.GET.get('page', 1)

            # 把当前的页码数转换成整数类型
            page = int(page)
            try:
                goodslist = paginator.page(page)  # 获取当前页码的记录
            except PageNotAnInteger:
                goodslist = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
            except EmptyPage:
                goodslist = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

            # data_num 当前页数据数目
            data_num = len(paginator.page(page).object_list)

            # page为当前页
            data = {
                'goods_lists': goodslist,
                'brandlist': brandlist,
                'classification': classification,
                'page': page,
                'p': paginator,
                'data_num': data_num
            }
            return render(request, 'admin/goodsList.html', data)
        else:
            return HttpResponseRedirect('/goods_manage/goodsList/')


def category_list(request):
    # 分类列表
    category_list = Classification.objects.all()
    #生成paginator对象,定义每页显示1条记录
    paginator = Paginator(category_list, PAGE_DATA_NUMBER)
    # 从前端获取当前的页码数,默认为1
    page = request.GET.get('page', 1)

    # 把当前的页码数转换成整数类型
    page = int(page)
    try:
        category_lists = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        category_lists = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        category_lists = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

    # data_num 当前页数据数目
    data_num = len(paginator.page(page).object_list)

    # page为当前页
    data = {
        'category_lists': category_lists,
        'page': page,
        'p': paginator,
        'data_num': data_num

    }
    return render(request, 'admin/categoryList.html', data)



def category_add(request):
    if request.method == 'GET':
        return render(request, 'admin/categoryAdd.html')

    # 添加分类
    if request.method == 'POST':

        category_lists = request.POST.get('cat_name').split(',')
        categoryLists = Classification.objects.all()

        for category in category_lists:
            # 判断分类是否存在
            for categoryList in categoryLists:
                if category == categoryList.name:
                    msg = '{0}分类已存在,添加失败'.format(category)
                    return render(request, 'admin/categoryAdd.html', {'msg': msg})
            Classification.objects.create(
                name=category
            )

        return render(request, 'admin/categoryAdd.html', {'OK': 'OK'})


def category_change(request):
    # 改变分类名称
    myName = request.POST.get('myName')
    content = request.POST.get('content')
    category_list = Classification.objects.all()
    for cat in category_list:
        if content == cat.name:
            data = {
                'code': 200,
                'msg': '修改失败,该分类已存在'
            }
            return JsonResponse(data)
    category = Classification.objects.filter(name=myName).first()
    category.name = content # 改变数据
    category.save() # 存储

    data = {
        'code': 200,
        'msg': '改变成功'
    }

    return JsonResponse(data)


def category_remove(request):
    # 删除该分类
    myName = request.POST.get('myName')

    category = Classification.objects.filter(name=myName).first()

    category.delete()

    data = {
        'code': 200,
        'msg': '删除成功'
    }

    return JsonResponse(data)

def brand_list(request):
    # 品牌列表
    brand_list = Brand.objects.all()

    #生成paginator对象,定义每页显示2条记录
    paginator = Paginator(brand_list, PAGE_DATA_NUMBER)
    # 从前端获取当前的页码数,默认为1
    page = request.GET.get('page', 1)

    # 把当前的页码数转换成整数类型
    page = int(page)
    try:
        brand_lists = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        brand_lists = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        brand_lists = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

    # data_num 当前页数据数目
    data_num = len(paginator.page(page).object_list)

    # page为当前页
    data = {
        'brand_lists': brand_lists,
        'page': page,
        'p': paginator,
        'data_num': data_num

    }
    return render(request, 'admin/brandList.html', data)



def brand_add(request):

    if request.method == 'GET':
        return render(request, 'admin/brandAdd.html')

    # 添加品牌
    if request.method == 'POST':

        brand_lists = request.POST.get('brand_name').split(',')
        brandLists = Brand.objects.all()
        for brand in brand_lists:
            for brandList in brandLists:
                if brand == brandList.name:
                    msg = '{0}品牌已存在,添加失败'.format(brand)
                    return render(request, 'admin/categoryAdd.html', {'msg': msg})
            Brand.objects.create(
                name=brand
            )

        return render(request, 'admin/brandAdd.html', {'OK': 'OK'})


def brand_change(request):
    # 改变品牌名称
    myName = request.POST.get('myName')
    content = request.POST.get('content')
    brand_list = Brand.objects.all()
    for brands in brand_list:
        if content == brands.name:
            data = {
                'code': 200,
                'msg': '修改失败,该品牌已存在'
            }
            return JsonResponse(data)

    brand = Brand.objects.filter(name=myName).first()
    brand.name = content # 改变数据
    brand.save() # 存储

    data = {
        'code': 200,
        'msg': '改变成功'
    }

    return JsonResponse(data)


def brand_remove(request):
    # 删除该品牌
    myName = request.POST.get('myName')

    brand = Brand.objects.filter(name=myName).first()

    brand.delete()

    data = {
        'code': 200,
        'msg': '删除成功'
    }

    return JsonResponse(data)


def brand_search(request):
    # 品牌查询
    if request.method == 'GET':
        return HttpResponseRedirect('/goods_manage/brandList/')

    if request.method == 'POST':
        brand_name = request.POST.get('brand_name')
        brand_list = Brand.objects.filter(name__contains=brand_name)
        paginator = Paginator(brand_list, PAGE_DATA_NUMBER)
        page = request.GET.get('page', 1)
        page = int(page)
        try:
            brand_lists = paginator.page(page)  # 获取当前页码的记录
        except PageNotAnInteger:
            brand_lists = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
        except EmptyPage:
            brand_lists = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

        # data_num 当前页数据数目
        data_num = len(paginator.page(page).object_list)

        # page为当前页
        data = {
            'brand_lists': brand_lists,
            'page': page,
            'p': paginator,
            'data_num': data_num

        }
        return render(request, 'admin/brandList.html', data)

