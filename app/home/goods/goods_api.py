"""
商品详情页面
AUTH:
DATE:
"""
from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from app.models import Goods, Focus, HistoryPrice, Comments
from app.serializers import GoodsSerializer, HistorySerializer, CommentsSerializer
from django.db import connection


def goods(request, pk):
    return render(request, 'home/goods.html')


def goods_list(request):
    if request.method == 'GET':
        all_goods = Goods.objects.all()
        serializer = GoodsSerializer(all_goods, many=True)
        return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def goods_detail(request, pk):
    if request.method == 'GET':
        good = Goods.objects.get(pk=pk)
        serializer = GoodsSerializer(good)
        data = {
            'status': status.HTTP_200_OK,
            'msg': '请求成功',
            'data': serializer.data
        }
        return Response(data, content_type='json')


@api_view(['GET'])
def is_focus(request, pk):
    if request.method == 'GET':
        user_id = 2
        if Focus.objects.filter(goods_id=pk, user_id=user_id):
            is_focus = True
        else:
            is_focus = False
        data = {
            'status': status.HTTP_200_OK,
            'msg': '请求成功',
            'data': {'is_focus': is_focus}
        }

        return Response(data, content_type='json')


@api_view(['POST'])
def focus(request):
    # user_id = request.session['user_id']
    if request.method == 'POST':
        ticket = request.COOKIE.get('ticket')
        user_id = 2
        item_id = request.POST.get('item_id')
        if Focus.objects.filter(goods_id=item_id, user_id=user_id):
            is_focus = False
            focus_instance = Focus.objects.get(goods_id=item_id, user_id=user_id)
            focus_instance.delete()
        else:
            Focus.objects.create(goods_id=item_id, user_id=user_id)
            is_focus = True
        data = {
            'status': status.HTTP_200_OK,
            'msg': '请求成功',
            'data': {'is_focus': is_focus}
        }
        return Response(data, content_type='json')


@api_view(['GET'])
def history_data(request, pk):
    if request.method == 'GET':
        history = HistoryPrice.objects.get(good_id=pk)
        dates = history.date
        prices = history.price
        serializer = HistorySerializer(history)
        data = {
            'status': status.HTTP_200_OK,
            'msg': '请求成功',
            'data': serializer.data
        }
        return Response(data, content_type='json')


@api_view(['GET', 'POST'])
def comments(request, pk):
    if request.method == 'GET':
        item_comments = Comments.objects.filter(goods_id=pk)
        scores = [comment.score for comment in item_comments]
        cati = item_comments.annotate(score_count=Count('score')).values('score', 'score_count')
        ave_score = sum(scores)/len(scores)
        good_comments = 0
        mid_comments = 0
        bad_comments = 0
        for score in scores:
            if score == 5:
                good_comments += 1
            elif 3 <= score <= 4:
                mid_comments += 1
            else:
                bad_comments += 1
        good_comments_percent = good_comments * 100 // len(scores)
        mid_comments_percent = mid_comments * 100 // len(scores)
        bad_comments_percent = 100 - good_comments_percent - mid_comments_percent
        score_data = {
            'ave_score': ave_score,
            'good_comments': good_comments,
            'mid_comments': mid_comments,
            'bad_comments': bad_comments,
            'good_comments_percent': good_comments_percent,
            'mid_comments_percent': mid_comments_percent,
            'bad_comments_percent': bad_comments_percent,
        }
        serializer = CommentsSerializer(item_comments, many=True)
        data = {
            'status': status.HTTP_200_OK,
            'msg': '请求成功',
            'data': serializer.data,
            'score_data': score_data
        }
        return Response(data, content_type='json')
    if request.method == 'POST':
        serializer = CommentsSerializer(data=request.data)
        item = Goods.objects.get(id=pk)
        serializer.is_valid()
        if serializer.is_valid():
            try:
                serializer.save()
                item.comments_amount += 1
                item.save()
            except Exception as e:
                print(e)
            data = {
                'status': status.HTTP_201_CREATED,
                'msg': '请求成功',
                'data': serializer.data
            }
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# def goods_detail(request, pk):
#     """
#     Retrieve, update or delete
#     """
#     try:
#         good = Goods.objects.get(pk=pk)
#     except Goods.DoesNotExist:
#         return HttpResponse(status=404)
#
#     if request.method == 'GET':
#         serializer = GoodsSerializer(good)
#         return JsonResponse(serializer.data, status=status.HTTP_200_OK)
#
#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = GoodsSerializer(good, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)
#
#     elif request.method == 'DELETE':
#         good.delete()
#         return HttpResponse(status=204)
