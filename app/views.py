from datetime import datetime
from io import BytesIO

import xlrd
import xlwt
from django.core.exceptions import ValidationError
from django.forms import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from GoodBuy.settings import BASE_DIR
from app.models import Hot
from app.untils.verify_code import VerifyCode
# Create your views here.

def verify_code(request):
    verify_code = VerifyCode(width=147, height=45)
    request.session['v_code'] = verify_code.verify_code
    v_image = verify_code.verify_image
    f = BytesIO()
    v_image.save(f, 'jpeg')
    return HttpResponse(f.getvalue(), content_type='image/jpeg')


def my_test(request):
    if request.method == 'GET':
        hots = Hot.objects.all()
        my_list = ['word', 'count']
        ws = save_to_excel('热门对比', hots, my_list)
        bio = BytesIO()
        ws.save(bio)
        return HttpResponse(bio.getvalue(), content_type='application/vnd.ms-excel')
        # return render(request,'admin/test.html')
    if request.method == 'POST':
        data = {}
        file = request.FILES['excel']
        with open(BASE_DIR+'/static/files/hello.xls', 'wb') as pic:
            for c in file.chunks():
                pic.write(c)
        wb = xlrd.open_workbook(BASE_DIR+'/static/files/hello.xls')
        table = wb.sheets()[0]
        nrows = table.nrows
        ncols = table.ncols
        if file.name.split('.')[-1] not in ['xls', 'xlsx']:
            raise JsonResponse({'msg':'文件上传错误'})


        hots = Hot.objects.all()
        my_list = ['word','count']
        ws = save_to_excel('热门对比',hots,my_list)
        bio = BytesIO()
        ws.save(bio)
        return HttpResponse(bio.getvalue(),content_type='application/vnd.ms-excel')


def save_to_excel(table_name,list_obj, my_list):
    ws = xlwt.Workbook(encoding='utf-8')
    w = ws.add_sheet(table_name)
    row = 0
    for obj in list_obj:
        for i,val in enumerate(my_list):
            if row == 0:
                w.write(row, i, val)
            else:
                obj_dict = model_to_dict(obj)
                w.write(row, i, obj_dict.get(val))
        row += 1
    return ws

